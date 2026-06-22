"""
主程序入口
完整的 Instagram + TikTok 网红数据采集与评估流程
"""
import sys
import os
from typing import List
from instagram_profile_scraper import InstagramProfileScraper
from tiktok_creator_scraper import TikTokCreatorScraper
from kol_scoring_model import KOLScoringModel
from config import BRIGHTDATA_API_KEY


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def check_api_key():
    """检查 API Key 是否已设置"""
    if BRIGHTDATA_API_KEY == "YOUR_BRIGHTDATA_API_KEY_HERE":
        print("❌ 错误：BRIGHTDATA_API_KEY 未设置！")
        print("\n📋 设置步骤：")
        print("1. 复制 .env.example 并重命名为 .env")
        print("   命令: cp .env.example .env  (Linux/Mac)")
        print("   或手动创建 .env 文件")
        print("\n2. 在 .env 文件中替换以下内容：")
        print("   BRIGHTDATA_API_KEY=你的_API_Key")
        print("\n3. 获取 API Key 的方式：")
        print("   - 登录 Bright Data 官网: https://www.brightdata.com/")
        print("   - 进入控制台 -> Web Scraper API")
        print("   - 生成新的 API Token")
        print("\n4. 保存 .env 文件后重新运行本程序")
        print("=" * 70)
        return False
    return True


def scrape_instagram_influencers(usernames: List[str]) -> List[dict]:
    """
    采集 Instagram 网红数据
    """
    print_header("第一步: Instagram 网红数据采集")
    
    scraper = InstagramProfileScraper()
    print(f"\n目标用户: {', '.join(usernames)}")
    print(f"总共需要采集: {len(usernames)} 个账户\n")
    
    profiles = scraper.fetch_profiles_batch(usernames)
    return profiles


def scrape_tiktok_creators(usernames: List[str]) -> List[dict]:
    """
    采集 TikTok 创作者数据
    """
    print_header("第二步: TikTok 创作者数据采集")
    
    scraper = TikTokCreatorScraper()
    print(f"\n目标创作者: {', '.join(usernames)}")
    print(f"总共需要采集: {len(usernames)} 个账户\n")
    
    creators = scraper.fetch_creators_batch(usernames)
    return creators


def process_instagram_data(profiles: List[dict]) -> str:
    """
    处理 Instagram 数据
    """
    print_header("第三步: Instagram 数据清洗与评分")
    
    processor = KOLScoringModel()
    processor.load_data(profiles, "instagram")
    processor.clean_data()
    processor.calculate_engagement_rate()
    processor.calculate_kol_score()
    processor.rank_kols(min_score=40)
    
    # 打印统计信息
    summary = processor.get_summary()
    print("\n[数据统计]")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value}")
    
    # 导出数据
    print("\n[数据导出]")
    csv_path = processor.export_to_csv("instagram_influencers.csv")
    excel_path = processor.export_to_excel("instagram_influencers.xlsx")
    
    return excel_path if excel_path else csv_path


def process_tiktok_data(creators: List[dict]) -> str:
    """
    处理 TikTok 数据
    """
    print_header("第四步: TikTok 数据清洗与评分")
    
    processor = KOLScoringModel()
    processor.load_data(creators, "tiktok")
    processor.clean_data()
    processor.calculate_engagement_rate()
    processor.calculate_kol_score()
    processor.rank_kols(min_score=40)
    
    # 打印统计信息
    summary = processor.get_summary()
    print("\n[数据统计]")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value}")
    
    # 导出数据
    print("\n[数据导出]")
    csv_path = processor.export_to_csv("tiktok_creators.csv")
    excel_path = processor.export_to_excel("tiktok_creators.xlsx")
    
    return excel_path if excel_path else csv_path


def main():
    """
    主程序流程
    """
    print_header("开始: 海外网红数据采集与评估系统")
    
    # 1. 检查 API Key
    if not check_api_key():
        print("❌ 程序退出")
        sys.exit(1)
    
    print("✓ API Key 配置正确")
    
    # ==================== 自定义你的采集目标 ====================
    # 💡 在下方修改这些列表，替换为你想采集的真实用户名
    
    # Instagram 用户名列表（去掉 @ 符号）
    instagram_usernames = [
        "cristiano",      # 示例：C罗
        "leomessi",       # 示例：梅西
        "selenagomez",    # 示例：塞琳娜·戈麦斯
        # 👉 添加你的目标用户名：
        # "your_username_1",
        # "your_username_2",
    ]
    
    # TikTok 用户名列表（去掉 @ 符号）
    tiktok_usernames = [
        "addisonre",      # 示例：Addison Rae（1700万粉丝）
        "dixiedamelio",   # 示例：Dixie D'Amelio（1300万粉丝）
        "zoelaverne",     # 示例：Zoe Laverne（3900万粉丝）
        # 👉 添加你的目标用户名：
        # "your_tiktok_username_1",
        # "your_tiktok_username_2",
    ]
    
    # ==================== 执行采集流程 ====================
    
    try:
        # 第一步：采集 Instagram 数据
        print("\n[正在执行采集...]")
        ig_profiles = scrape_instagram_influencers(instagram_usernames)
        
        if not ig_profiles:
            print("⚠️  Instagram 数据采集失败或无结果")
            print("   可能原因：")
            print("   1. API Key 无效 - 检查 .env 文件")
            print("   2. Bright Data 账户余额不足")
            print("   3. 网络连接问题")
            print("   4. 用户名不存在或已禁用")
        else:
            ig_output = process_instagram_data(ig_profiles)
        
        # 第二步：采集 TikTok 数据
        tk_profiles = scrape_tiktok_creators(tiktok_usernames)
        
        if not tk_profiles:
            print("⚠️  TikTok 数据采集失败或无结果")
        else:
            tk_output = process_tiktok_data(tk_profiles)
        
        # 最后总结
        print_header("采集完成！")
        
        if ig_profiles:
            print(f"\n✓ Instagram: 成功采集 {len(ig_profiles)} 个账户")
            print(f"  输出文件: {ig_output}")
        
        if tk_profiles:
            print(f"\n✓ TikTok: 成功采集 {len(tk_profiles)} 个账户")
            print(f"  输出文件: {tk_output}")
        
        print("\n📊 后续操作:")
        print("   1. 打开导出的 Excel 文件审阅数据")
        print("   2. 根据 KOL 评分选择合作对象")
        print("   3. 联系高评分的网红进行商务合作")
        print("\n💡 提示:")
        print("   - 修改 main.py 中的 instagram_usernames 和 tiktok_usernames 列表来采集不同用户")
        print("   - 调整 config.py 中的 KOL_SCORING_WEIGHTS 来改变评分权重")
        
    except KeyboardInterrupt:
        print("\n⚠️  程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()