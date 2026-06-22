"""
TikTok 数据采集模块
调用 Bright Data Scraper API 获取 TikTok 创作者的实时数据
"""
import requests
import json
import time
from typing import List, Dict, Optional
from config import (
    BRIGHTDATA_API_KEY,
    BRIGHTDATA_API_URL,
    TIKTOK_DATASET_ID,
    TIKTOK_FIELDS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
)


class TikTokCreatorScraper:
    """TikTok 数据采集类"""

    def __init__(self):
        # ⚠️ 重要：确保 BRIGHTDATA_API_KEY 在 .env 文件中已正确设置
        self.api_key = BRIGHTDATA_API_KEY
        self.api_url = BRIGHTDATA_API_URL
        self.dataset_id = TIKTOK_DATASET_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def fetch_creator_profile(self, username: str) -> Optional[Dict]:
        """
        根据用户名采集 TikTok 创作者数据
        
        参数：
            username (str): TikTok 用户名，不含 @ 符号
            
        返回：
            Dict: 包含创作者信息的字典，如果失败返回 None
        """
        print(f"[TikTok] 正在采集创作者: {username}")

        # 构建 TikTok 用户页面 URL
        url = f"https://www.tiktok.com/@{username}/"
        
        payload = {
            "url": url,
        }

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    params={
                        "dataset_id": self.dataset_id,
                        "format": "json"
                    },
                    headers=self.headers,
                    timeout=REQUEST_TIMEOUT,
                )

                if response.status_code == 200:
                    data = response.json()
                    # 处理不同格式的响应
                    if isinstance(data, list) and len(data) > 0:
                        # 如果返回的是列表，取第一个元素
                        creator = data[0]
                        if isinstance(creator, dict):
                            # 尝试多个可能的字段名来获取粉丝数
                            follower_count = creator.get("follower_count") or creator.get("followers") or creator.get("user", {}).get("follower_count") or 0
                            print(f"✓ 成功采集: {username} (粉丝数: {follower_count:,})")
                            return creator
                        else:
                            print(f"✗ 数据格式错误")
                            return None
                    elif isinstance(data, dict):
                        if data.get("success") and data.get("results"):
                            creator = data["results"][0]
                            # 尝试多个可能的字段名来获取粉丝数
                            follower_count = creator.get("follower_count") or creator.get("followers") or creator.get("user", {}).get("follower_count") or 0
                            print(f"✓ 成功采集: {username} (粉丝数: {follower_count:,})")
                            return creator
                        else:
                            print(f"✗ 未找到创作者: {username}")
                            return None
                    else:
                        print(f"✗ 未知的响应格式: {type(data)}")
                        return None

                elif response.status_code == 429:  # Rate Limited
                    print(f"⚠️  触发速率限制，等待 {RETRY_DELAY} 秒后重试...")
                    time.sleep(RETRY_DELAY)

                elif response.status_code == 401:
                    print("❌ API Key 无效或已过期！请检查 .env 文件中的 BRIGHTDATA_API_KEY")
                    return None

                elif response.status_code == 403:
                    print("❌ 权限不足！请检查你的 Bright Data 账户配额")
                    return None

                else:
                    print(f"❌ API 错误: {response.status_code} - {response.text}")
                    if attempt < MAX_RETRIES - 1:
                        print(f"  准备进行第 {attempt + 2} 次尝试...")
                        time.sleep(RETRY_DELAY)

            except requests.exceptions.Timeout:
                print(f"⏱️  请求超时，等待后重试... (尝试 {attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)

            except requests.exceptions.ConnectionError:
                print(f"🔌 网络连接错误，等待后重试... (尝试 {attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)

            except Exception as e:
                print(f"❌ 未预期的错误: {str(e)}")
                return None

        print(f"✗ 在 {MAX_RETRIES} 次尝试后仍然失败")
        return None

    def fetch_creators_batch(self, usernames: List[str]) -> List[Dict]:
        """
        批量采集多个 TikTok 创作者数据
        
        参数：
            usernames (List[str]): TikTok 用户名列表
            
        返回：
            List[Dict]: 采集成功的创作者数据列表
        """
        results = []
        total = len(usernames)

        for idx, username in enumerate(usernames, 1):
            print(f"\n[进度] {idx}/{total}")
            creator = self.fetch_creator_profile(username)

            if creator:
                results.append(creator)
                # 为避免触发平台限制，建议在每次请求之间加入延迟
                time.sleep(2)

        return results

    def fetch_hashtag_videos(self, hashtag: str, limit: int = 100) -> Optional[List[Dict]]:
        """
        采集特定 Hashtag 下的视频列表
        
        参数：
            hashtag (str): 话题标签，不含 # 符号
            limit (int): 返回结果数量限制
            
        返回：
            List[Dict]: 视频数据列表
        """
        print(f"[TikTok] 正在采集 Hashtag: #{hashtag}")

        payload = {
            "dataset_id": self.dataset_id,
            "query": hashtag,
            "parse": True,
            "limit": limit,
        }

        try:
            response = requests.post(
                f"{self.api_url}/query",
                json=payload,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    videos = data.get("results", [])
                    print(f"✓ 成功采集 {len(videos)} 条视频")
                    return videos
                else:
                    print(f"✗ 采集失败: {data.get('message', 'Unknown error')}")
                    return None

            elif response.status_code == 401:
                print("❌ API Key 无效！请检查 .env 文件")
                return None

            else:
                print(f"❌ API 错误: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return None


if __name__ == "__main__":
    # 测试代码
    scraper = TikTokCreatorScraper()

    # 采集单个创作者
    print("=" * 60)
    print("测试 1: 采集单个 TikTok 创作者")
    print("=" * 60)
    creator = scraper.fetch_creator_profile("khaby.lame")

    if creator:
        print("\n采集结果:")
        print(json.dumps(creator, indent=2, ensure_ascii=False))

    # 采集多个创作者
    print("\n" + "=" * 60)
    print("测试 2: 批量采集多个创作者")
    print("=" * 60)
    usernames = ["khaby.lame", "charlidamelio", "tiktok"]
    results = scraper.fetch_creators_batch(usernames)

    print(f"\n成功采集 {len(results)} 个创作者的数据")