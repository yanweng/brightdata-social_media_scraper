"""
数据导出模块
将 KOL 评分结果导出为 CSV、Excel 或 Google Sheets
"""
import pandas as pd
from typing import Optional
from datetime import datetime
from config import OUTPUT_DIR


class ExportToSheets:
    """数据导出类"""

    def __init__(self, df: pd.DataFrame, platform: str = "instagram"):
        """
        初始化导出器
        
        参数：
            df (pd.DataFrame): 要导出的数据框
            platform (str): 平台标识
        """
        self.df = df
        self.platform = platform

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


if __name__ == "__main__":
    # 演示代码
    print("=" * 60)
    print("数据导出演示")
    print("=" * 60)

    # 模拟数据
    sample_data = [
        {
            "rank": 1,
            "username": "user1",
            "followers": 100000,
            "engagement_rate_pct": 5.2,
            "kol_score": 85.5,
        },
        {
            "rank": 2,
            "username": "user2",
            "followers": 200000,
            "engagement_rate_pct": 3.8,
            "kol_score": 78.2,
        },
    ]

    df = pd.DataFrame(sample_data)
    exporter = ExportToSheets(df, "instagram")
    
    # 导出为 CSV
    csv_path = exporter.export_to_csv("demo_export.csv")
    
    # 导出为 Excel
    excel_path = exporter.export_to_excel("demo_export.xlsx")
    
    print("\n✓ 导出完成！")