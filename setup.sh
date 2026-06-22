#!/bin/bash
# 快速启动脚本（Linux/Mac）
# 使用方式: bash setup.sh

set -e

echo "========================================"
echo "  海外网红数据采集系统 - 快速设置"
echo "========================================"

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ 检测到 Python $python_version"

# 创建虚拟环境
echo ""
echo "[1/4] 创建虚拟环境..."
python3 -m venv venv
echo "✓ 虚拟环境创建完成"

# 激活虚拟环境
echo ""
echo "[2/4] 激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活"

# 安装依赖
echo ""
echo "[3/4] 安装依赖包..."
pip install -q -r requirements.txt
echo "✓ 依赖安装完成"

# 创建 .env 文件
echo ""
echo "[4/4] 设置 API Key..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ .env 文件已创建"
    echo ""
    echo "⚠️  请完成以下步骤："
    echo "  1. 打开 .env 文件"
    echo "  2. 替换 BRIGHTDATA_API_KEY=YOUR_BRIGHTDATA_API_KEY_HERE"
    echo "  3. 将其替换为你的真实 API Key"
    echo ""
    echo "获取 API Key: https://www.brightdata.com/"
else
    echo "✓ .env 文件已存在"
fi

echo ""
echo "========================================"
echo "✅ 设置完成！"
echo "========================================"
echo ""
echo "后续步骤："
echo "1. 编辑 main.py 中的 instagram_usernames 和 tiktok_usernames"
echo "2. 运行命令启动程序:"
echo "   source venv/bin/activate"
echo "   python main.py"
