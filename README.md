# 海外网红数据采集与评估系统

基于 Bright Data 的完整 Instagram + TikTok 网红情报采集解决方案。

> 🌟 **[点击此处注册 Bright Data，获取免费测试额度](YOUR_BRIGHTDATA_AFFILIATE_LINK_HERE)**

## 📋 项目结构

```
social_media_scraper/
├── main.py                      # 主程序入口
├── config.py                    # 配置文件（API Key、权重等）
├── instagram_profile_scraper.py # Instagram 采集模块
├── tiktok_creator_scraper.py    # TikTok 采集模块
├── kol_scoring_model.py         # 数据清洗与 KOL 评分模块
├── export_to_sheets.py          # 数据导出模块（CSV/Excel/Google Sheets）
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量示例（需要复制为 .env）
├── output/                      # 输出目录（自动创建）
└── README.md                    # 本文件
```

## 🚀 快速开始

### 1️⃣ 环境准备

**Python 版本要求**: 3.9 或以上

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2️⃣ 配置 API Key

⚠️ **最重要的一步！**

#### 方法 A: 使用 .env 文件（推荐）

```bash
# 复制示例文件
cp .env.example .env

# 用编辑器打开 .env，修改以下内容：
BRIGHTDATA_API_KEY=YOUR_BRIGHTDATA_API_KEY
```

#### 方法 B: 获取 Bright Data API Key

1. 访问 [Bright Data 官网](YOUR_BRIGHTDATA_AFFILIATE_LINK_HERE)
2. 登录或注册账户
3. 进入控制台 → Web Scraper API
4. 点击"生成 API Token"
5. 复制你的 API Key
6. 粘贴到 `.env` 文件中

```env
BRIGHTDATA_API_KEY=YOUR_BRIGHTDATA_API_KEY
```

### 3️⃣ 修改采集目标

编辑 `main.py` 中的用户名列表：

```python
# Instagram 用户名列表（去掉 @ 符号）
instagram_usernames = [
    "cristiano",      # 示例
    "leomessi",       # 示例
    # 👉 添加你的目标用户：
    "your_target_username_1",
    "your_target_username_2",
]

# TikTok 用户名列表（去掉 @ 符号）
tiktok_usernames = [
    "khaby.lame",     # 示例
    "charlidamelio",  # 示例
    # 👉 添加你的目标用户：
    "your_tiktok_username_1",
    "your_tiktok_username_2",
]
```

### 4️⃣ 运行程序

```bash
python main.py
```

**预期输出：**

```
======================================================================
  开始: 海外网红数据采集与评估系统
======================================================================
✓ API Key 配置正确

======================================================================
  第一步: Instagram 网红数据采集
======================================================================

目标用户: cristiano, leomessi, selenagomez
总共需要采集: 3 个账户

[Instagram] 正在采集用户: cristiano
✓ 成功采集: cristiano (粉丝数: 615000000)
...

✓ CSV 文件已保存: ./output/instagram_influencers.csv
✓ Excel 文件已保存: ./output/instagram_influencers.xlsx
```

## 📊 输出文件

程序执行成功后，会在 `output/` 目录中生成：

- `instagram_influencers.csv` - Instagram 数据（CSV 格式）
- `instagram_influencers.xlsx` - Instagram 数据（Excel 格式）
- `tiktok_creators.csv` - TikTok 数据（CSV 格式）
- `tiktok_creators.xlsx` - TikTok 数据（Excel 格式）

每个文件包含字段：

| 字段 | 说明 |
|------|------|
| rank | 排名（按 KOL 评分从高到低） |
| username/author_name | 用户名 |
| followers/follower_count | 粉丝数 |
| engagement_rate_pct | 互动率（%） |
| kol_score | KOL 商业价值评分（0-100） |

## ⚙️ 配置说明

### config.py 中可调整的参数

#### 1. 评分权重（KOL_SCORING_WEIGHTS）

```python
KOL_SCORING_WEIGHTS = {
    "followers": 0.25,        # 粉丝数权重
    "engagement_rate": 0.35,  # 互动率权重（最重要）
    "post_frequency": 0.15,   # 发布频率权重
    "verification": 0.15,     # 认证状态权重
    "niche_relevance": 0.10,  # 领域相关性权重
}
```

**调整建议：**
- 如果优先考虑大号，增加 `followers` 权重
- 如果优先考虑活跃度，增加 `engagement_rate` 权重
- 如果只关心垂直领域博主，增加 `niche_relevance` 权重

#### 2. API 超时和重试

```python
REQUEST_TIMEOUT = 30      # 单个请求超时时间（秒）
MAX_RETRIES = 3          # 失败后的重试次数
RETRY_DELAY = 5          # 重试间隔（秒）
```

## 🔧 故障排除

### ❌ 问题 1: "API Key 未设置"

**解决方案：**
```bash
# 确认 .env 文件存在
ls -la .env

# 确认 BRIGHTDATA_API_KEY 不是占位符
cat .env | grep BRIGHTDATA_API_KEY
```

### ❌ 问题 2: "API 错误 401 - Unauthorized"

**可能原因：**
- API Key 过期或无效
- 复制时包含了空格

**解决方案：**
1. 在 Bright Data 控制台重新生成 API Key
2. 检查 .env 文件中 Key 的前后没有空格

### ❌ 问题 3: "API 错误 429 - Too Many Requests"

**可能原因：**
- 请求过于频繁
- 触发了平台速率限制

**解决方案：**
```python
# 在 main.py 中增加延迟
time.sleep(5)  # 每个请求之间等待 5 秒
```

### ❌ 问题 4: "未找到用户"

**可能原因：**
- 用户名拼写错误
- 账户已被删除或禁用

**解决方案：**
- 在 Instagram/TikTok 上验证用户名是否存在
- 确保用户名不含 @ 符号

## 📈 数据分析建议

### 1. 互动率解读

```
互动率 < 1%   → 粉丝可能注水
1% - 3%      → 普通账户（较低热度）
3% - 5%      → 正常账户（推荐合作）
5% - 10%     → 高热度账户（优先合作）
> 10%        → 超级活跃账户（顶级合作对象）
```

### 2. KOL 评分解读

```
评分 < 40    → 不推荐合作
40 - 60      → 可考虑合作
60 - 80      → 优质合作对象
> 80        → 顶级合作对象
```

## 🔒 安全建议

1. **不要将 API Key 上传到 Git**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **定期轮换 API Key**
   - 每月在 Bright Data 控制台重新生成一次

3. **监控 API 使用量**
   - 登录 Bright Data 控制台定期检查用量

## 📚 进阶用法

### 自定义采集字段

在 `config.py` 中修改：

```python
INSTAGRAM_FIELDS = [
    "username",
    "followers",
    "engagement_rate",
    "your_custom_field",  # 添加自定义字段
]
```

### 批量采集 Hashtag

```python
from instagram_profile_scraper import InstagramProfileScraper

scraper = InstagramProfileScraper()
posts = scraper.fetch_hashtag_posts("beauty", limit=100)
```

### 导出到 Google Sheets

```python
# 安装 gspread
pip install gspread google-auth-oauthlib

# 然后在 export_to_sheets.py 中添加导出函数
```

## 📞 获取帮助

1. **检查 API 文档**: https://www.brightdata.com/products/web-scraper/api
2. **Bright Data 支持**: 登录控制台 → Support
3. **常见问题**: 见本文档的"故障排除"部分

## 📝 许可证

本项目仅供学习和个人研究使用。使用本工具采集数据时，请遵守目标网站的 Terms of Service。

## 🎯 功能特性

✅ 自动化采集 Instagram + TikTok 网红数据  
✅ 智能数据清洗和去重  
✅ KOL 商业价值评分模型  
✅ Excel/CSV 格式导出  
✅ 错误重试和异常处理  
✅ 灵活的配置系统  
✅ 详细的日志输出  

---

> 🌟 **[立即注册 Bright Data，开启你的海外网红数据采集之旅！](YOUR_BRIGHTDATA_AFFILIATE_LINK_HERE)**

祝你成功！💪