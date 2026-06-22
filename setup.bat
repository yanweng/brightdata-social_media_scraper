@echo off
REM 快速启动脚本（Windows）
REM 使用方式: 双击运行或在 PowerShell 中执行 setup.bat

setlocal enabledelayedexpansion

echo ========================================
echo   海外网红数据采集系统 - 快速设置
echo ========================================

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到 Python，请先安装 Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ 检测到 Python %PYTHON_VERSION%

REM 创建虚拟环境
echo.
echo [1/4] 创建虚拟环境...
if not exist venv (
    python -m venv venv
    if %errorlevel% equ 0 (
        echo ✓ 虚拟环境创建完成
    ) else (
        echo ❌ 虚拟环境创建失败
        pause
        exit /b 1
    )
) else (
    echo ✓ 虚拟环境已存在
)

REM 激活虚拟环境
echo.
echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat
if %errorlevel% equ 0 (
    echo ✓ 虚拟环境已激活
) else (
    echo ❌ 虚拟环境激活失败
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo [3/4] 安装依赖包...
pip install -q -r requirements.txt
if %errorlevel% equ 0 (
    echo ✓ 依赖安装完成
) else (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 创建 .env 文件
echo.
echo [4/4] 设置 API Key...
if not exist .env (
    copy .env.example .env >nul
    echo ✓ .env 文件已创建
    echo.
    echo ⚠️  请完成以下步骤：
    echo   1. 打开 .env 文件（用记事本或VS Code）
    echo   2. 找到这一行: BRIGHTDATA_API_KEY=YOUR_BRIGHTDATA_API_KEY_HERE
    echo   3. 替换为你的真实 API Key
    echo.
    echo 获取 API Key: https://www.brightdata.com/
) else (
    echo ✓ .env 文件已存在
)

echo.
echo ========================================
echo ✅ 设置完成！
echo ========================================
echo.
echo 后续步骤：
echo 1. 编辑 main.py 中的 instagram_usernames 和 tiktok_usernames
echo 2. 运行命令启动程序：
echo    python main.py
echo.
pause
