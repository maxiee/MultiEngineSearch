# MultiEngineSearch (mes)

一个遵循Unix哲学原则的多搜索引擎统一命令行界面工具。

## 概述

MultiEngineSearch (mes) 是一个轻量级、可扩展的命令行工具，提供了查询多个搜索引擎的统一接口。它专注于做好一件事：通过一致的输出格式和灵活的配置选项在不同引擎间进行搜索。

## 特性

- **多搜索引擎支持**: 目前支持 DuckDuckGo 和 Google Custom Search API，计划支持 Bing 等引擎
- **API限流跟踪**: Google 搜索引擎支持实时API使用量监控和限流信息显示
- **灵活的输出格式**: 支持 JSON 和简单 (simple) 格式输出，包含限流信息
- **时间筛选**: 支持按时间范围筛选搜索结果 (最近一天/周/月/年)
- **Unix友好**: 支持管道、重定向，遵循Unix约定
- **可配置**: 支持搜索引擎配置和参数调整
- **可扩展**: 基于工厂模式的架构，便于添加新的搜索引擎
- **轻量级**: 最小依赖，快速执行
- **错误处理**: 优雅的错误处理和用户友好的提示

## 安装

使用Poetry安装项目：

```bash
# 克隆仓库
git clone https://github.com/yourusername/MultiEngineSearch.git
cd MultiEngineSearch

# 使用 Poetry 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

## 快速开始

```bash
# 基本搜索 (默认使用 DuckDuckGo)
mes search "python编程教程"

# 使用 Google 搜索引擎 (带限流监控)
mes search "机器学习" --engine google --limit 5
# JSON格式查看详细限流信息
mes search "AI新闻" --engine google --output json

# 输出为JSON格式
mes search "网页开发" --output json --limit 5

# 显示详细信息
mes search "深度学习" --verbose --limit 5

# 时间筛选搜索
mes search "最新AI新闻" --time d --limit 10   # 搜索最近一天的结果
mes search "本周技术新闻" --time w             # 搜索最近一周的结果

# 查看可用的搜索引擎
mes config --list

# 查看版本信息
mes version
```

## 使用方法

### 搜索命令

```bash
mes search [查询内容] [选项]
```

**选项:**
- `--engine, -e`: 指定搜索引擎 (目前支持: duckduckgo, google)
- `--limit, -l`: 返回结果数量限制 (1-100，默认10)
- `--output, -o`: 输出格式 (json, simple，默认simple)
- `--time, -t`: 时间筛选范围 (d=最近一天, w=最近一周, m=最近一月, y=最近一年，默认无限制)
- `--verbose, -v`: 显示详细信息

**示例:**
```bash
# 基本搜索 (使用默认 DuckDuckGo 引擎)
mes search "Python教程"

# 指定引擎和结果数量
mes search "机器学习" --engine duckduckgo --limit 5
mes search "人工智能" --engine google --limit 5     # 需要配置API密钥

# JSON格式输出
mes search "AI新闻" --output json --verbose

# 时间筛选搜索
mes search "AI最新进展" --time d --limit 10    # 最近一天的结果
mes search "机器学习新闻" --time w              # 最近一周的结果
mes search "深度学习论文" --time m              # 最近一月的结果
mes search "人工智能发展" --time y              # 最近一年的结果

# 组合使用时间筛选和其他选项
mes search "ChatGPT新闻" --time w --output json --limit 5 --verbose
```

### 配置命令

```bash
mes config [选项]
```

**选项:**
- `--list, -l`: 列出所有可用的搜索引擎
- `--set-default`: 设置默认搜索引擎

**示例:**
```bash
# 列出可用引擎
mes config --list

# 设置默认引擎 (功能开发中)
mes config --set-default duckduckgo
```

### 版本信息

```bash
# 显示版本信息
mes version
```

## 使用示例

### 基本搜索
```bash
$ mes search "Python编程教程" --limit 3
🔍 找到 3 个搜索结果:

 1. Python入门教程：从零基础到精通的完整指南 - 知乎
    🔗 https://zhuanlan.zhihu.com/p/1914418882829091976
    📄 Python 作为一门简洁优雅、功能强大的编程语言,近年来备受欢迎...
    🔍 来源: duckduckgo

 2. Python 基础教程 - 菜鸟教程
    🔗 https://www.runoob.com/python/python-tutorial.html
    📄 本教程适合想从零开始学习 Python 编程语言的开发人员...
    🔍 来源: duckduckgo

 3. Python 教程 — Python 3.13.4 文档
    🔗 https://docs.python.org/zh-cn/3/tutorial/index.html
    📄 Python 解释器易于扩展，使用 C 或 C++...
    🔍 来源: duckduckgo
```

### 时间筛选搜索
```bash
# 时间筛选参数说明
--time d    # 最近一天 (past day)
--time w    # 最近一周 (past week)  
--time m    # 最近一月 (past month)
--time y    # 最近一年 (past year)
# 不指定 --time 参数则不限制时间范围

# 实际使用示例
mes search "Python 3.12新特性" --time m      # 查找最近一月内的Python 3.12相关内容
mes search "区块链最新动态" --time w --output json    # 最近一周的区块链新闻，JSON格式输出
mes search "ChatGPT更新" --time d --limit 5   # 最近一天ChatGPT相关信息，限制5条结果
```

### JSON 格式输出 (包含限流信息)
```bash
$ mes search "机器学习" --engine google --output json --limit 2
{
  "results": [
    {
      "title": "Machine Learning | Google AI",
      "url": "https://ai.google/education/",
      "description": "Learn about machine learning and artificial intelligence...",
      "engine": "google"
    },
    {
      "title": "机器学习 - 维基百科",
      "url": "https://zh.wikipedia.org/wiki/机器学习",
      "description": "机器学习（英語： machine learning ）是人工智能的一个分支...",
      "engine": "google"
    }
  ],
  "count": 2,
  "rate_limit": {
    "daily_limit": 100,
    "requests_used": 3,
    "requests_remaining": 97,
    "limit_exceeded": false
  }
}
```

### Simple 格式输出 (包含限流信息)
```bash
$ mes search "Python编程" --engine google --limit 2
🔍 找到 2 个搜索结果:

 1. Welcome to Python.org
    🔗 https://www.python.org/
    📄 The official home of the Python Programming Language.
    🔍 来源: google

 2. Python Tutorial - W3Schools
    🔗 https://www.w3schools.com/python/
    📄 Well organized and easy to understand Web building tutorials...
    🔍 来源: google

📊 API 使用情况:
    • 每日限额: 100 次
    • 已使用: 5 次
    • 剩余: 95 次
```

### 查看可用引擎
```bash
$ mes config --list
📋 可用的搜索引擎:
  • duckduckgo
  • google

💡 计划支持的搜索引擎:
  • bing (开发中)
  • baidu (开发中)
```

### Google 搜索引擎配置 (可选)

如果要使用 Google 搜索引擎，需要配置 Google Custom Search API：

## API 限流监控

MultiEngineSearch 现在为 Google 搜索引擎提供了实时的 API 使用量监控和限流信息显示。

### 限流信息包括：

- **每日限额**: Google API 每日免费调用限额（默认 100 次）
- **已使用**: 累计已使用的请求次数（跨会话持久保存）
- **剩余次数**: 剩余可用的请求次数
- **是否超额**: 标识是否已达到每日限额

### 特性优势：

1. **实时监控**: 每次搜索后都会显示最新的 API 使用情况
2. **多格式支持**: 在 JSON 和 Simple 两种输出格式中都包含限流信息
3. **用户友好**: 提供直观的使用情况显示和警告提示
4. **智能管理**: 帮助用户合理分配 API 配额，避免超额

### 使用示例：

```bash
# 使用 Google 搜索，查看限流信息
mes search "Python 教程" --engine google --limit 3

# JSON 格式查看详细限流数据
mes search "AI 新闻" --engine google --output json
```

⚠️ **重要说明**：
- 限流计数器使用持久化存储（~/.mes_google_quota.json），跨程序重启保持准确
- 配额重置基于太平洋时间（US/Pacific），与Google API官方周期同步
- 每天太平洋时间午夜自动重置配额计数器
- 虽然无法获取Google服务器的实时配额，但本地跟踪非常准确
- 大的查询可能触发多个 API 请求（分页），每个都会计入限流

更多详细信息请查看：[API 限流功能文档](docs/RATE_LIMITING.md)

### Google 搜索引擎配置步骤：

1. **获取 API 密钥**：
   - 访问 [Google Cloud Console](https://console.cloud.google.com/)
   - 创建新项目或选择现有项目
   - 启用 Custom Search API
   - 创建 API 密钥

2. **创建自定义搜索引擎**：
   - 访问 [Programmable Search Engine](https://programmablesearchengine.google.com/)
   - 创建新的搜索引擎
   - 获取搜索引擎 ID (Search Engine ID)

3. **设置环境变量**：
   ```bash
   export MES_GOOGLE_API_KEY="your_api_key_here"
   export MES_GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id_here"
   ```

   或在 `.bashrc` / `.zshrc` 中添加：
   ```bash
   # Google Search API 配置
   export MES_GOOGLE_API_KEY="your_api_key_here"
   export MES_GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id_here"
   ```

**注意**: Google 每天免费提供 100 次 API 调用额度，超出后按 $5/1000 次调用收费。

## 技术栈

- **Python 3.13+**: 现代Python特性支持
- **Typer**: 强大的CLI框架，提供丰富的命令行功能
- **Poetry**: 现代Python依赖管理和打包工具
- **DuckDuckGo Search**: 免费的搜索API，无需API密钥
- **Google Custom Search API**: Google官方搜索API，需要API密钥
- **Requests**: HTTP库，用于API请求
- **Rich**: 美观的终端输出和格式化 (通过Typer集成)

## 项目结构

```
MultiEngineSearch/
├── src/
│   └── multienginesearch/
│       ├── __init__.py          # 包初始化和导出
│       ├── cli.py               # CLI入口和命令定义
│       └── engines.py           # 搜索引擎接口和实现
├── tests/                       # 测试文件
│   ├── test_cli.py             # CLI功能测试
│   └── test_engines.py         # 搜索引擎测试
├── docs/                        # 文档
│   ├── duckduckgo_search.md    # DuckDuckGo API文档
│   └── 使用 Google Search API 优雅地搜索互联网.md  # Google API文档
├── pyproject.toml              # Poetry配置和项目元数据
└── README.md                   # 项目文档
```

## 开发计划

- [x] 实现DuckDuckGo搜索引擎接口 ✅
- [x] 基础CLI命令框架 ✅  
- [x] 多种输出格式支持 (JSON, Simple) ✅
- [x] 错误处理和用户提示 ✅
- [x] 完整的测试覆盖 ✅
- [x] 时间筛选功能: 支持按时间范围筛选搜索结果 ✅
- [x] 实现Google搜索引擎接口 ✅
- [ ] 实现Bing搜索引擎接口  
- [ ] 实现Baidu搜索引擎接口
- [ ] 添加配置文件支持
- [ ] 实现结果缓存机制
- [ ] 添加搜索历史功能
- [ ] 支持搜索结果过滤和排序
- [ ] 添加更多输出格式（CSV、XML等）
- [ ] 添加代理支持
- [ ] 支持并行多引擎搜索

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

## 许可证

MIT License
