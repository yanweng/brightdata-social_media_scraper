# 🔐 API Key 配置完整指南

## 📍 需要填写 API Key 的位置

本项目中有 **3 个地方** 需要填写你的 Bright Data API Key。

### ✅ 位置 1: `.env` 文件（**最重要**）

**文件路径**: `social_media_scraper/.env`

**步骤**:
1. 复制 `.env.example` 并重命名为 `.env`
   ```bash
   cp .env.example .env
   ```

2. 用编辑器打开 `.env`，找到这一行：
   ```
   BRIGHTDATA_API_KEY=YOUR_BRIGHTDATA_API_KEY_HERE
   ```

3. 替换为你的真实 API Key：
   ```
   BRIGHTDATA_API_KEY=sk_1234567890abcdefghijklmnopqrst
   ```

4. 保存文件

**⚠️ 重要**: 
- `.env` 文件已添加到 `.gitignore`，不会被上传到 Git
- 不要硬编码 API Key 到代码中
- 不要将 `.env` 文件提交到版本控制

---

### ✅ 位置 2: `config.py` 文件

**文件路径**: `social_media_scraper/config.py`

该文件会自动从 `.env` 加载 API Key：

```python
# config.py 第 7 行
BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY", "YOUR_BRIGHTDATA_API_KEY_HERE")
```

**⚠️ 说明**:
- 这里的 `YOUR_BRIGHTDATA_API_KEY_HERE` 是 **占位符/默认值**
- 程序启动时会自动从 `.env` 文件读取真实 Key
- **不需要手动修改** `config.py` 中的 API Key

---

### ✅ 位置 3: `instagram_scraper.py` 和 `tiktok_scraper.py`

**文件路径**: 
- `social_media_scraper/instagram_scraper.py` 第 23-26 行
- `social_media_scraper/tiktok_scraper.py` 第 23-26 行

代码片段：
```python
def __init__(self):
    # ⚠️ 重要：确保 BRIGHTDATA_API_KEY 在 .env 文件中已正确设置
    self.api_key = BRIGHTDATA_API_KEY
    self.api_url = BRIGHTDATA_API_URL
    self.headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json",
    }
```

**⚠️ 说明**:
- 这里的 `BRIGHTDATA_API_KEY` 是从 `config.py` **自动导入** 的
- **不需要手动修改** 这些文件
- 只需确保 `.env` 文件中的 Key 正确即可

---

## 🎯 快速检查清单

运行程序之前，请检查：

- [ ] `.env` 文件已创建（通过复制 `.env.example`）
- [ ] `.env` 文件中填写了真实的 `BRIGHTDATA_API_KEY`
- [ ] API Key 不含前后空格或引号
- [ ] `.env` 文件的格式为：`KEY=VALUE`（无引号）
- [ ] Python 依赖已安装：`pip install -r requirements.txt`

## 📋 如何获取 Bright Data API Key

### 步骤 1: 注册/登录 Bright Data
- 访问: https://www.brightdata.com/
- 使用 Google、GitHub 账户快速注册或用邮箱注册

### 步骤 2: 进入控制台
- 登录后点击右上角 "Dashboard"（控制台）
- 或直接访问: https://app.brightdata.com/

### 步骤 3: 创建 API Token
- 左侧菜单: **Products** → **Web Scraper**
- 或直接访问: https://app.brightdata.com/products/web_scraper

- 点击 **"API"** 标签
- 点击 **"Create API Token"** 按钮
- 选择 token 权限（建议选择完整访问）
- 复制生成的 API Key

### 步骤 4: 粘贴到 .env 文件
```
BRIGHTDATA_API_KEY=sk_你的_API_Key
```

---

## 🔍 测试 API Key 是否正确

### 方法 1: 直接运行主程序
```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 运行程序
python main.py
```

程序启动时会验证 API Key：
- ✅ **正确**: 显示 `✓ API Key 配置正确`，继续执行
- ❌ **错误**: 显示 `❌ 错误：BRIGHTDATA_API_KEY 未设置！`，需要检查 `.env` 文件

### 方法 2: 单独测试 Instagram 采集
```bash
python instagram_scraper.py
```

### 方法 3: 单独测试 TikTok 采集
```bash
python tiktok_scraper.py
```

---

## ⚠️ 常见错误与解决方案

### 错误 1: "BRIGHTDATA_API_KEY 未设置"

**原因**: `.env` 文件中的 Key 是占位符

**解决**:
```bash
cat .env | grep BRIGHTDATA_API_KEY
# 应该显示: BRIGHTDATA_API_KEY=sk_xxxxx（实际值）
# 如果显示: BRIGHTDATA_API_KEY=YOUR_BRIGHTDATA_API_KEY_HERE（占位符）
```

→ 用真实 Key 替换占位符

### 错误 2: "API 错误 401 - Unauthorized"

**原因**: API Key 无效或已过期

**解决**:
1. 重新登录 Bright Data 控制台
2. 检查 API Key 是否仍然有效
3. 如过期，生成新的 Key
4. 更新 `.env` 文件

### 错误 3: ".env 文件找不到"

**原因**: `.env` 文件不存在

**解决**:
```bash
# 创建 .env 文件
cp .env.example .env

# 编辑并填写 API Key
nano .env  # 或用其他编辑器
```

### 错误 4: "API Key 中含有空格或特殊字符"

**原因**: 复制时不小心包含了空格或引号

**解决**:
```
❌ 错误格式:
BRIGHTDATA_API_KEY = sk_xxxxx  # 含有空格
BRIGHTDATA_API_KEY="sk_xxxxx"   # 含有引号

✅ 正确格式:
BRIGHTDATA_API_KEY=sk_xxxxx  # 无空格，无引号
```

---

## 🔒 安全最佳实践

1. **永远不要在代码中硬编码 API Key**
   ```python
   # ❌ 不要这样做
   API_KEY = "sk_1234567890"
   
   # ✅ 应该这样做
   API_KEY = os.getenv("BRIGHTDATA_API_KEY")
   ```

2. **定期轮换 API Key**
   - 每月在 Bright Data 控制台重新生成一次

3. **监控 API 使用量**
   - 登录 Bright Data 控制台
   - 检查当月的 API 调用数和剩余配额

4. **不要将 .env 提交到 Git**
   - `.gitignore` 已包含 `.env`
   - 使用 `git check-ignore .env` 验证

5. **如果不小心泄露了 Key**
   - 立即在 Bright Data 控制台删除该 token
   - 生成新的 Key
   - 更新所有使用该 Key 的地方

---

## 📞 需要帮助？

- **Bright Data 官网**: https://www.brightdata.com/
- **API 文档**: https://www.brightdata.com/products/web-scraper/api
- **联系支持**: 登录控制台 → Help → Support

---

✅ 完成以上步骤后，你就可以运行 `python main.py` 了！
