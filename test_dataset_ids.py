"""
测试不同的 Bright Data 数据集 ID，找出最适合采集 TikTok 粉丝数据的 ID
"""
import requests
import json
import time
from config import BRIGHTDATA_API_KEY, BRIGHTDATA_API_URL

# 待测试的数据集 ID 列表
DATASET_IDS = {
    "gd_lu702nij2f790tmv9h": "ID 1",
    "gd_lkf2st302ap89utw5k": "ID 2",
    "gd_l1villgoiiidt09ci": "ID 3 (当前使用)",
    "gd_m45m1u911dsa4274pi": "ID 4",
    "gd_lk5ns7kz21pck8jpis": "ID 5",
    "gd_lyclm20il4r5helnj": "ID 6",
    "gd_l1vikfch901nx3by4": "ID 7 (Instagram用的)",
    "gd_ltppn085pokosxh13": "ID 8",
}

def test_dataset(dataset_id: str, username: str = "addisonre"):
    """
    测试单个数据集 ID
    """
    url = f"https://www.tiktok.com/@{username}/"
    
    payload = {
        "url": url,
    }
    
    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(
            BRIGHTDATA_API_URL,
            json=payload,
            params={
                "dataset_id": dataset_id,
                "format": "json"
            },
            headers=headers,
            timeout=30,
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # 尝试提取粉丝数
            follower_count = None
            field_found = None
            
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
            elif isinstance(data, dict):
                if "results" in data and len(data.get("results", [])) > 0:
                    item = data["results"][0]
                else:
                    item = data
            else:
                return {"status": "error", "message": f"未知的响应格式"}
            
            if isinstance(item, dict):
                # 尝试多个可能的字段名
                possible_fields = ["follower_count", "followers", "follower", "fans", "fans_count"]
                for field in possible_fields:
                    if field in item and item[field]:
                        follower_count = item[field]
                        field_found = field
                        break
                
                # 如果还没找到，显示所有可用的数值字段
                if follower_count is None:
                    numeric_fields = {k: v for k, v in item.items() if isinstance(v, (int, float)) and v > 0}
                    return {
                        "status": "partial",
                        "message": "找到数据但缺少粉丝数字段",
                        "numeric_fields": numeric_fields,
                        "all_keys": list(item.keys())
                    }
                else:
                    return {
                        "status": "success",
                        "follower_count": follower_count,
                        "field_name": field_found
                    }
            else:
                return {"status": "error", "message": "响应不是字典"}
        
        elif response.status_code == 429:
            return {"status": "rate_limited", "message": "触发速率限制"}
        elif response.status_code == 401:
            return {"status": "auth_error", "message": "API Key 无效"}
        else:
            return {"status": "http_error", "code": response.status_code, "message": response.text[:200]}
    
    except requests.exceptions.Timeout:
        return {"status": "timeout", "message": "请求超时"}
    except Exception as e:
        return {"status": "exception", "message": str(e)}


def main():
    """
    主测试函数
    """
    print("=" * 80)
    print("  Bright Data 数据集 ID 测试")
    print("  目标: 找出能返回真实粉丝数的 TikTok 数据集")
    print("=" * 80)
    print()
    
    results = {}
    successful_ids = []
    partial_ids = []
    failed_ids = []
    
    for dataset_id, label in DATASET_IDS.items():
        print(f"🔍 测试 {label}: {dataset_id}")
        
        result = test_dataset(dataset_id)
        results[dataset_id] = result
        
        if result["status"] == "success":
            print(f"   ✅ 成功！粉丝数: {result['follower_count']:,} (字段: {result['field_name']})")
            successful_ids.append((dataset_id, label, result))
        elif result["status"] == "partial":
            print(f"   ⚠️  找到数据但缺少粉丝数")
            print(f"      可用字段: {list(result.get('numeric_fields', {}).keys())[:5]}")
            partial_ids.append((dataset_id, label, result))
        else:
            print(f"   ❌ {result['status']}: {result.get('message', '未知错误')}")
            failed_ids.append((dataset_id, label, result))
        
        print()
        time.sleep(2)  # 避免频繁请求触发速率限制
    
    # 打印总结
    print("\n" + "=" * 80)
    print("  📊 测试结果汇总")
    print("=" * 80)
    
    print(f"\n✅ 成功获取粉丝数的 ID ({len(successful_ids)}):")
    for dataset_id, label, result in successful_ids:
        print(f"   • {label}: {dataset_id}")
        print(f"     粉丝数: {result['follower_count']:,}, 字段: {result['field_name']}")
    
    print(f"\n⚠️  找到数据但缺少粉丝数的 ID ({len(partial_ids)}):")
    for dataset_id, label, result in partial_ids:
        print(f"   • {label}: {dataset_id}")
        if result.get("numeric_fields"):
            print(f"     可用数值字段: {list(result['numeric_fields'].keys())}")
    
    print(f"\n❌ 无法使用的 ID ({len(failed_ids)}):")
    for dataset_id, label, result in failed_ids:
        print(f"   • {label}: {dataset_id} - {result.get('message', '未知错误')}")
    
    print("\n" + "=" * 80)
    if successful_ids:
        best_id, best_label, best_result = successful_ids[0]
        print(f"\n🎯 推荐: 使用 {best_label} ({best_id})")
        print(f"   这个 ID 能正确返回粉丝数数据！")
    else:
        print("\n💡 提示: 没有 ID 能直接返回粉丝数。")
        if partial_ids:
            print("   但有些 ID 返回了数据，可能需要调整字段提取逻辑。")


if __name__ == "__main__":
    main()
