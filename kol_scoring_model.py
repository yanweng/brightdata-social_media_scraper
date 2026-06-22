"""
数据处理与 KOL 评分模块
- 清洗和去重采集数据
- 计算互动率、发布频率等关键指标
- 应用 KOL 商业价值评分权重模型
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import (
    MIN_ENGAGEMENT_RATE,
    MAX_ENGAGEMENT_RATE,
    KOL_SCORING_WEIGHTS,
    OUTPUT_DIR,
)


class KOLScoringModel:
    """数据处理与评分类"""

    def __init__(self):
        self.df = None
        self.platform = None

    def load_data(self, data_list: List[Dict], platform: str = "instagram") -> pd.DataFrame:
        """
        加载采集数据到 DataFrame
        
        参数：
            data_list (List[Dict]): 采集的原始数据列表
            platform (str): 平台标识 ('instagram' 或 'tiktok')
            
        返回：
            pd.DataFrame: 转换后的数据框
        """
        self.platform = platform.lower()
        
        if not data_list:
            print("⚠️  数据列表为空")
            return pd.DataFrame()

        self.df = pd.DataFrame(data_list)
        print(f"✓ 已加载 {len(self.df)} 条 {platform} 数据")
        
        return self.df

    def clean_data(self) -> pd.DataFrame:
        """
        数据清洗：
        - 去除重复行
        - 处理缺失值
        - 数据类型转换
        """
        if self.df is None or self.df.empty:
            print("⚠️  无数据可清洗")
            return pd.DataFrame()

        initial_count = len(self.df)

        # 1. 去重（基于用户名或用户ID）
        username_col = "username" if "username" in self.df.columns else "author_name"
        if username_col in self.df.columns:
            self.df = self.df.drop_duplicates(subset=[username_col])
            print(f"✓ 去重完成：移除了 {initial_count - len(self.df)} 条重复记录")

        # 2. 处理缺失值和数据类型转换
        # 定义需要转换为数值的字段
        numeric_fields = [
            "followers", "follower_count", "following", "following_count",
            "posts", "video_count", "likes", "like_count", "comments",
            "bio", "biography", "engagement_rate", "bio_link"
        ]
        
        for col in numeric_fields:
            if col in self.df.columns:
                # 提取数值，处理各种类型的输入
                def extract_numeric(x):
                    if isinstance(x, (int, float)):
                        return x
                    elif isinstance(x, str):
                        try:
                            return float(x)
                        except:
                            return 0
                    elif isinstance(x, dict):
                        # 如果是字典，尝试提取第一个值
                        try:
                            return float(list(x.values())[0])
                        except:
                            return 0
                    else:
                        return 0
                
                self.df[col] = self.df[col].apply(extract_numeric).fillna(0).astype(int)

        # 文本列填充为 'N/A'
        self.df = self.df.fillna("N/A")

        print(f"✓ 清洗完成：最终保留 {len(self.df)} 条有效数据")
        return self.df

    def calculate_engagement_rate(self) -> pd.DataFrame:
        """
        计算互动率（Engagement Rate）
        
        互动率 = (点赞数 + 评论数) / 粉丝数 / 发布次数
        范围：0% - 100%
        """
        if self.df is None or self.df.empty:
            print("⚠️  无数据可计算")
            return self.df

        print(f"[{self.platform}] 计算互动率...")

        if self.platform == "instagram":
            # Instagram：(likes + comments) / followers / posts
            if all(col in self.df.columns for col in ["likes", "comments", "followers", "posts"]):
                self.df["engagement_rate"] = (
                    (self.df["likes"].fillna(0) + self.df["comments"].fillna(0))
                    / (self.df["followers"] + 1)  # +1 避免除以0
                    / (self.df["posts"] + 1)
                )
            else:
                # 如果缺少具体字段，使用 0（不再使用模拟数据）
                self.df["engagement_rate"] = 0
                print("  ℹ️  未找到详细字段，互动率设置为 0")

        elif self.platform == "tiktok":
            # TikTok：(点赞数) / (粉丝数 * 视频数)
            if all(col in self.df.columns for col in ["like_count", "follower_count", "video_count"]):
                self.df["engagement_rate"] = (
                    self.df["like_count"].fillna(0)
                    / (self.df["follower_count"] + 1)
                    / (self.df["video_count"] + 1)
                )
            else:
                self.df["engagement_rate"] = 0
                print("  ℹ️  未找到详细字段，互动率设置为 0")

        # 限制范围在 [0%, 100%]
        self.df["engagement_rate"] = self.df["engagement_rate"].clip(
            MIN_ENGAGEMENT_RATE, MAX_ENGAGEMENT_RATE
        )
        self.df["engagement_rate_pct"] = self.df["engagement_rate"] * 100

        print(f"✓ 互动率计算完成")
        return self.df

    def calculate_kol_score(self) -> pd.DataFrame:
        """
        计算 KOL 商业价值评分（KOL Score）
        基于加权评分模型：
        - 粉丝数 (25%)
        - 互动率 (35%)
        - 发布频率 (15%)
        - 认证状态 (15%)
        - 领域相关性 (10%)
        
        总分范围：0-100 分
        """
        if self.df is None or self.df.empty:
            print("⚠️  无数据可评分")
            return self.df

        print(f"[{self.platform}] 计算 KOL 评分...")

        scores = pd.DataFrame(index=self.df.index)

        # 1. 粉丝数得分（归一化到 0-1）
        follower_col = "followers" if "followers" in self.df.columns else "follower_count"
        if follower_col in self.df.columns:
            # 确保是数值型
            self.df[follower_col] = pd.to_numeric(self.df[follower_col], errors="coerce").fillna(0)
            max_followers = self.df[follower_col].max()
            if max_followers > 0:
                scores["followers_score"] = self.df[follower_col] / max_followers
            else:
                scores["followers_score"] = 0
        else:
            scores["followers_score"] = 0

        # 2. 互动率得分（已归一化在 0-1）
        if "engagement_rate" in self.df.columns:
            self.df["engagement_rate"] = pd.to_numeric(self.df["engagement_rate"], errors="coerce").fillna(0)
            scores["engagement_score"] = self.df["engagement_rate"] / MAX_ENGAGEMENT_RATE
        else:
            scores["engagement_score"] = 0

        # 3. 发布频率得分
        posts_col = "posts" if "posts" in self.df.columns else "video_count"
        if posts_col in self.df.columns:
            # 确保是数值型
            self.df[posts_col] = pd.to_numeric(self.df[posts_col], errors="coerce").fillna(0)
            max_posts = self.df[posts_col].max()
            if max_posts > 0:
                scores["frequency_score"] = self.df[posts_col] / max_posts
            else:
                scores["frequency_score"] = 0
        else:
            scores["frequency_score"] = 0

        # 4. 认证状态得分
        verified_col = "is_verified" if "is_verified" in self.df.columns else "is_verified"
        if verified_col in self.df.columns:
            scores["verification_score"] = self.df[verified_col].astype(bool).astype(int)
        else:
            scores["verification_score"] = 0

        # 5. 领域相关性得分（演示：基于简单规则）
        # 实际应用中可集成 NLP 模型判断账号内容与目标市场的相关性
        scores["niche_score"] = np.random.uniform(0.3, 1.0, len(self.df))

        # 计算加权总分
        weights = KOL_SCORING_WEIGHTS
        self.df["kol_score"] = (
            scores["followers_score"] * weights["followers"] +
            scores["engagement_score"] * weights["engagement_rate"] +
            scores["frequency_score"] * weights["post_frequency"] +
            scores["verification_score"] * weights["verification"] +
            scores["niche_score"] * weights["niche_relevance"]
        ) * 100  # 转换为 0-100 分制

        # 四舍五入到两位小数
        self.df["kol_score"] = self.df["kol_score"].round(2)

        print(f"✓ KOL 评分计算完成，平均分: {self.df['kol_score'].mean():.2f}")
        return self.df

    def rank_kols(self, min_score: float = 50) -> pd.DataFrame:
        """
        根据 KOL 评分排序，筛选出优质 KOL
        
        参数：
            min_score (float): 最低评分阈值（0-100）
            
        返回：
            pd.DataFrame: 排序和筛选后的数据
        """
        if self.df is None or self.df.empty:
            return self.df

        # 按评分从高到低排序
        self.df = self.df.sort_values("kol_score", ascending=False).reset_index(drop=True)
        self.df["rank"] = range(1, len(self.df) + 1)

        # 筛选高于阈值的 KOL
        high_quality = self.df[self.df["kol_score"] >= min_score]
        print(f"✓ 排名完成：共 {len(high_quality)} 个 KOL 评分超过 {min_score} 分")

        return self.df

    def export_to_csv(self, filename: Optional[str] = None) -> str:
        """
        导出数据到 CSV 文件
        
        参数：
            filename (str): 文件名（可选）
            
        返回：
            str: 保存的文件路径
        """
        if self.df is None or self.df.empty:
            print("⚠️  无数据可导出")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.platform}_kol_data_{timestamp}.csv"

        filepath = f"{OUTPUT_DIR}/{filename}"

        try:
            self.df.to_csv(filepath, index=False, encoding="utf-8-sig")
            print(f"✓ CSV 文件已保存: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")
            return ""

    def export_to_excel(self, filename: Optional[str] = None) -> str:
        """
        导出数据到 Excel 文件（支持格式化）
        
        参数：
            filename (str): 文件名（可选）
            
        返回：
            str: 保存的文件路径
        """
        if self.df is None or self.df.empty:
            print("⚠️  无数据可导出")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.platform}_kol_data_{timestamp}.xlsx"

        filepath = f"{OUTPUT_DIR}/{filename}"

        try:
            # 选择要导出的关键列
            key_columns = ["rank", "username" if "username" in self.df.columns else "author_name",
                          "followers" if "followers" in self.df.columns else "follower_count",
                          "engagement_rate_pct", "kol_score"]
            
            export_df = self.df[[col for col in key_columns if col in self.df.columns]]

            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
                export_df.to_excel(writer, sheet_name=self.platform.capitalize(), index=False)

                # 格式化
                worksheet = writer.sheets[self.platform.capitalize()]
                for column in worksheet.columns:
                    max_length = 15
                    worksheet.column_dimensions[column[0].column_letter].width = max_length

            print(f"✓ Excel 文件已保存: {filepath}")
            return filepath

        except ImportError:
            print("⚠️  缺少 openpyxl 库，请运行: pip install openpyxl")
            return ""
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")
            return ""

    def get_summary(self) -> Dict:
        """
        获取数据汇总统计
        """
        if self.df is None or self.df.empty:
            return {}

        follower_col = "followers" if "followers" in self.df.columns else "follower_count"
        
        summary = {
            "总样本数": len(self.df),
            "平均粉丝数": self.df[follower_col].mean(),
            "最大粉丝数": self.df[follower_col].max(),
            "平均互动率": self.df.get("engagement_rate_pct", pd.Series([0])).mean(),
            "平均 KOL 评分": self.df["kol_score"].mean(),
            "评分最高": self.df["kol_score"].max(),
            "评分最低": self.df["kol_score"].min(),
        }

        return summary


if __name__ == "__main__":
    # 演示代码
    print("=" * 60)
    print("数据处理演示")
    print("=" * 60)

    # 模拟数据
    sample_data = [
        {
            "username": "user1",
            "followers": 100000,
            "posts": 150,
            "likes": 50000,
            "comments": 5000,
            "is_verified": True,
        },
        {
            "username": "user2",
            "followers": 200000,
            "posts": 200,
            "likes": 80000,
            "comments": 8000,
            "is_verified": True,
        },
    ]

    processor = KOLScoringModel()
    processor.load_data(sample_data, "instagram")
    processor.clean_data()
    processor.calculate_engagement_rate()
    processor.calculate_kol_score()
    processor.rank_kols(min_score=40)

    print("\n" + "=" * 60)
    print("数据汇总")
    print("=" * 60)
    summary = processor.get_summary()
    for key, value in summary.items():
        print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")