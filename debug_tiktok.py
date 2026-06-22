"""
调试 TikTok API 返回的实际数据结构
"""
import requests
import json
from config import BRIGHTDATA_API_KEY, BRIGHTDATA_API_URL, TIKTOK_DATASET_ID

def debug_tiktok_response():
    """获取并打印 TikTok API 返回的完整数据"""
    
    username = "addisonre"
    url = f"https://www.tiktok.com/@{username}/"
    
    payload = {
        "url": url,
    }
    
    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_KEY}",
        "Content-Type": "application/json",
    }
    
    print(f"🔍 调试 TikTok API - 用户: {username}")
    print(f"📤 请求 URL: {url}\n")
    
    response = requests.post(
        BRIGHTDATA_API_URL,
        json=payload,
        params={
            "dataset_id": TIKTOK_DATASET_ID,
            "format": "json"
        },
        headers=headers,
        timeout=30,
    )
    
    print(f"📥 响应状态码: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("📋 完整返回数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 如果是列表，显示第一个元素
        if isinstance(data, list) and len(data) > 0:
            print("\n\n🔎 第一个元素的所有字段:")
            first_item = data[0]
            if isinstance(first_item, dict):
                for key, value in first_item.items():
                    print(f"  {key}: {value} (类型: {type(value).__name__})")
        elif isinstance(data, dict):
            print("\n\n🔎 字典数据的所有键:")
            for key, value in data.items():
                if isinstance(value, (list, dict)):
                    print(f"  {key}: [复杂结构] (类型: {type(value).__name__})")
                else:
                    print(f"  {key}: {value} (类型: {type(value).__name__})")
    else:
        print(f"❌ 错误: {response.text}")

if __name__ == "__main__":
    debug_tiktok_response()
