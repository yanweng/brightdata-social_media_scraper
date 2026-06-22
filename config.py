"""
项目配置文件
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# ==================== Bright Data 配置 ====================
BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY", "YOUR_BRIGHTDATA_API_KEY_HERE")
BRIGHTDATA_API_URL = os.getenv("BRIGHTDATA_API_URL", "https://api.brightdata.com/datasets/v3/scrape")

# ==================== API 请求配置 ====================
REQUEST_TIMEOUT = 30  # 秒
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 5  # 重试延迟（秒）

# ==================== Instagram 采集配置 ====================
# Instagram API 数据集 ID（需要在 Bright Data 控制台查询）
INSTAGRAM_DATASET_ID = os.getenv("INSTAGRAM_DATASET_ID", "YOUR_INSTAGRAM_DATASET_ID")

# 要采集的 Instagram 数据字段
INSTAGRAM_FIELDS = [
    "username",
    "name", 
    "biography",
    "followers",
    "following",
    "posts",
    "is_verified",
    "profile_pic_url",
    "is_business_account",
    "category_name",
]

# ==================== TikTok 采集配置 ====================
# TikTok API 数据集 ID（需要在 Bright Data 控制台查询）
TIKTOK_DATASET_ID = os.getenv("TIKTOK_DATASET_ID", "YOUR_TIKTOK_DATASET_ID")

# 要采集的 TikTok 数据字段
TIKTOK_FIELDS = [
    "author_id",
    "author_name",
    "follower_count",
    "video_count",
    "like_count",
    "bio",
    "avatar",
    "is_verified",
]

# ==================== 数据处理配置 ====================
# 互动率计算方式
MIN_ENGAGEMENT_RATE = 0.02  # 最小互动率阈值（2%）
MAX_ENGAGEMENT_RATE = 1.0   # 最大互动率上限（100%）

# KOL 评分权重模型
KOL_SCORING_WEIGHTS = {
    "followers": 0.25,        # 粉丝数权重
    "engagement_rate": 0.35,  # 互动率权重（最重要）
    "post_frequency": 0.15,   # 发布频率权重
    "verification": 0.15,     # 认证状态权重
    "niche_relevance": 0.10,  # 领域相关性权重
}

# ==================== 输出配置 ====================
OUTPUT_DIR = "./output"
OUTPUT_FORMATS = ["csv", "excel"]  # 支持的输出格式

# 创建输出目录（如果不存在）
os.makedirs(OUTPUT_DIR, exist_ok=True)