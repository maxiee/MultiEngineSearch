# Google 搜索引擎限流功能文档

## 概述

MultiEngineSearch 现在为 Google 搜索引擎提供了限流跟踪功能。这个功能可以帮助用户监控 Google Custom Search API 的使用情况，避免超出每日免费额度。

## 新功能特性

### 1. 限流信息跟踪

Google 搜索引擎现在会在每次请求后返回以下限流信息：

- `daily_limit`: 每日API调用限额（默认100次）
- `requests_used`: 当前会话中已使用的请求次数
- `requests_remaining`: 剩余可用请求次数
- `limit_exceeded`: 是否已超出限额

### 2. 增强的搜索响应

引入了新的 `SearchResponse` 类来包装搜索结果和元数据：

```python
class SearchResponse:
    def __init__(self, results: List[SearchResult], rate_limit_info: Optional[Dict[str, Any]] = None):
        self.results = results
        self.rate_limit_info = rate_limit_info
```

### 3. 输出格式增强

两种输出格式都增加了限流信息显示：

#### Simple 格式
```
🔍 找到 3 个搜索结果:

 1. Python Tutorial - Real Python
    🔗 https://realpython.com/
    📄 Learn Python programming with our comprehensive tutorials
    🔍 来源: google

📊 API 使用情况:
    • 每日限额: 100 次
    • 已使用: 5 次
    • 剩余: 95 次
```

#### JSON 格式
```json
{
  "results": [
    {
      "title": "Python Tutorial - Real Python",
      "url": "https://realpython.com/",
      "description": "Learn Python programming with our comprehensive tutorials",
      "engine": "google"
    }
  ],
  "count": 1,
  "rate_limit": {
    "daily_limit": 100,
    "requests_used": 5,
    "requests_remaining": 95,
    "limit_exceeded": false
  }
}
```

## 使用方法

### 基本使用

```python
from multienginesearch.engines import GoogleEngine, format_results

# 创建引擎
engine = GoogleEngine()

# 执行搜索
response = engine.search("Python programming", limit=5)

# 检查限流信息
if response.rate_limit_info:
    rate_info = response.rate_limit_info
    print(f"已使用: {rate_info['requests_used']}/{rate_info['daily_limit']}")
    print(f"剩余: {rate_info['requests_remaining']} 次")

# 格式化输出
simple_output = format_results(response, "simple")
json_output = format_results(response, "json")
```

### CLI 使用

命令行工具会自动显示限流信息：

```bash
# 使用 Google 搜索
mes search "Python tutorial" --engine google --output simple

# JSON 格式输出
mes search "Python tutorial" --engine google --output json
```

### 监控API使用

```python
# 检查是否接近限额
if response.rate_limit_info:
    remaining = response.rate_limit_info['requests_remaining']
    if remaining < 10:
        print("⚠️ 警告: API配额即将用完!")
    elif remaining < 50:
        print("💡 提示: 请注意API使用量")
```

## 重要说明

### 限制和注意事项

1. **持久化跟踪**: 限流计数器使用持久化存储（~/.mes_google_quota.json），跨Python会话保持准确
2. **太平洋时区**: 配额重置使用Google API的官方时区（US/Pacific），自动处理PST/PDT切换
3. **每日重置**: 配额计数器在太平洋时间午夜自动重置
4. **本地跟踪**: 由于Google API不提供实时配额信息，我们使用本地跟踪系统
5. **准确性**: 本地跟踪非常准确，只要不手动修改配额文件
6. **分页请求**: 大的查询可能触发多个API请求，每个都会计入限流

### 兼容性

- **向后兼容**: DuckDuckGo 搜索引擎保持原有行为，不返回限流信息
- **代码兼容**: 所有现有代码无需修改即可工作
- **测试覆盖**: 包含完整的单元测试

## 最佳实践

### 1. 监控使用情况

```python
def smart_search(engine, query, limit=10):
    response = engine.search(query, limit)
    
    if response.rate_limit_info:
        rate_info = response.rate_limit_info
        usage_percent = (rate_info['requests_used'] / rate_info['daily_limit']) * 100
        
        if usage_percent > 80:
            print(f"⚠️ 警告: 已使用 {usage_percent:.1f}% 的API配额")
        
        return response
```

### 2. 智能降级

```python
from multienginesearch.engines import GoogleEngine, DuckDuckGoEngine

def adaptive_search(query, limit=10):
    google_engine = GoogleEngine()
    response = google_engine.search(query, limit)
    
    # 如果Google API用完，切换到DuckDuckGo
    if response.rate_limit_info and response.rate_limit_info['limit_exceeded']:
        print("Google API已达限额，切换到DuckDuckGo...")
        ddg_engine = DuckDuckGoEngine()
        return ddg_engine.search(query, limit)
    
    return response
```

### 3. 配额管理

```python
def check_quota_status(engine):
    # 执行一次小的测试搜索来获取限流信息
    test_response = engine.search("test", limit=1)
    
    if test_response.rate_limit_info:
        rate_info = test_response.rate_limit_info
        print(f"📊 API配额状态:")
        print(f"   总配额: {rate_info['daily_limit']}")
        print(f"   已使用: {rate_info['requests_used']}")
        print(f"   剩余: {rate_info['requests_remaining']}")
        
        return rate_info['requests_remaining'] > 0
    
    return True
```

## 示例代码

完整的示例代码请查看 `examples/demo_rate_limit.py`，该脚本演示了：

- 如何使用限流功能
- 不同输出格式的显示效果
- 与DuckDuckGo引擎的对比
- 最佳实践示例

运行示例：

```bash
cd examples
python demo_rate_limit.py
```

## 故障排除

### 常见问题

1. **环境变量未设置**
   ```
   ❌ Google Search API 需要设置环境变量
   ```
   解决方案：设置 `MES_GOOGLE_API_KEY` 和 `MES_GOOGLE_SEARCH_ENGINE_ID`

2. **API密钥无效**
   ```
   ❌ Google Search API 请求失败，状态码: 403
   ```
   解决方案：检查API密钥和搜索引擎ID是否正确

3. **超出配额**
   ```
   limit_exceeded: true
   ```
   解决方案：等待下一天或升级到付费计划

## 更新日志

### v0.2.2 (时区修复)
- ✅ 修复了配额重置时区问题，使用Google API的官方时区
- ✅ 添加了pytz依赖来处理时区转换
- ✅ 自动处理PST/PDT夏令时切换
- ✅ 配额重置现在基于太平洋时间（US/Pacific）
- ✅ 显示时区信息和精确的重置时间
- ✅ 避免了时区不匹配导致的超额风险

### v0.2.1 (配额跟踪修复)
- ✅ 修复了配额跟踪问题，不再始终显示99
- ✅ 实现了持久化配额跟踪（跨会话保持）
- ✅ 添加了每日配额自动重置功能
- ✅ 增加了配额重置时间显示
- ✅ 优化了错误处理和警告提示
- ✅ 添加了数据来源标识显示

### v0.2.0
- ✅ 添加GoogleEngine限流跟踪功能
- ✅ 引入SearchResponse封装类
- ✅ 增强simple和JSON输出格式
- ✅ 向后兼容现有代码
- ✅ 完整的测试覆盖
- ✅ 详细的文档和示例