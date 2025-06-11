# MultiEngineSearch (mse)

一个遵循Unix哲学原则的多搜索引擎统一命令行界面工具。

## 概述

MultiEngineSearch (mse) 是一个轻量级、可扩展的命令行工具，提供了查询多个搜索引擎的统一接口。它专注于做好一件事：通过一致的输出格式和灵活的配置选项在不同引擎间进行搜索。

## 特性

- **多搜索引擎支持**: 目前支持 DuckDuckGo，计划支持 Google、Bing 等引擎
- **灵活的输出格式**: 支持 JSON、表格 (table) 和简单 (simple) 格式输出
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
mse search "python编程教程"

# 使用指定搜索引擎
mse search "机器学习基础" --engine duckduckgo

# 输出为JSON格式
mse search "网页开发" --output json --limit 5

# 输出为表格格式
mse search "人工智能" --output table --limit 3

# 显示详细信息
mse search "深度学习" --verbose --limit 5

# 查看可用的搜索引擎
mse config --list

# 查看版本信息
mse version
```

## 使用方法

### 搜索命令

```bash
mse search [查询内容] [选项]
```

**选项:**
- `--engine, -e`: 指定搜索引擎 (目前支持: duckduckgo)
- `--limit, -l`: 返回结果数量限制 (1-100，默认10)
- `--output, -o`: 输出格式 (json, table, simple，默认simple)
- `--verbose, -v`: 显示详细信息

**示例:**
```bash
# 基本搜索 (使用默认 DuckDuckGo 引擎)
mse search "Python教程"

# 指定引擎和结果数量
mse search "机器学习" --engine duckduckgo --limit 5

# JSON格式输出
mse search "AI新闻" --output json --verbose

# 表格格式输出
mse search "数据科学" --output table --limit 3
```

### 配置命令

```bash
mse config [选项]
```

**选项:**
- `--list, -l`: 列出所有可用的搜索引擎
- `--set-default`: 设置默认搜索引擎

**示例:**
```bash
# 列出可用引擎
mse config --list

# 设置默认引擎 (功能开发中)
mse config --set-default duckduckgo
```

### 版本信息

```bash
# 显示版本信息
mse version
```

## 使用示例

### 基本搜索
```bash
$ mse search "Python编程教程" --limit 3
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

### JSON 格式输出
```bash
$ mse search "机器学习" --output json --limit 2
[
  {
    "title": "机器学习 - 维基百科，自由的百科全书",
    "url": "https://zh.wikipedia.org/wiki/机器学习",
    "description": "机器学习（英語： machine learning ）是人工智能的一个分支...",
    "engine": "duckduckgo"
  },
  {
    "title": "机器学习简介 - 菜鸟教程",
    "url": "https://www.runoob.com/ml/ml-intro.html",
    "description": "机器学习（Machine Learning）是人工智能（AI）的一个分支...",
    "engine": "duckduckgo"
  }
]
```

### 表格格式输出
```bash
$ mse search "人工智能" --output table --limit 2
┌─────────────────────────────────────────────────────────────────────┐
│                            搜索结果                                  │
├─────────────────────────────────────────────────────────────────────┤
│  1. 人工智能（智能科学与技术专业术语）_百度百科                                       │
│     🔗 https://baike.baidu.com/item/人工智能/9180                           │
│     📄 人工智能（Artificial Intelligence），英文缩写为AI...                    │
│     🔍 引擎: duckduckgo                                             │
├─────────────────────────────────────────────────────────────────────┤
│  2. 人工智能 - 维基百科，自由的百科全书                                          │
│     🔗 https://zh.wikipedia.org/wiki/人工智能                               │
│     📄 人工智能（英語： artificial intelligence ，缩写为 AI ）...              │
│     🔍 引擎: duckduckgo                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 详细模式
```bash
$ mse search "深度学习" --verbose --limit 2
正在搜索: 深度学习
搜索引擎: 默认 (DuckDuckGo)
结果限制: 2
输出格式: simple
🔍 正在使用 duckduckgo 搜索...
🔍 找到 2 个搜索结果:

 1. 深度学习（人工神经网络的研究的概念）_百度百科
    🔗 https://baike.baidu.com/item/深度学习/3729729
    📄 深度学习(Deep Learning)特指基于深层神经网络模型和方法的机器学习...
    🔍 来源: duckduckgo

 2. 深度学习 - 维基百科，自由的百科全书
    🔗 https://zh.wikipedia.org/wiki/深度学习
    📄 深度学习方法常常被视为黑盒，大多数的结论确认都由经验而非理论来确定...
    🔍 来源: duckduckgo
```

### 查看可用引擎
```bash
$ mse config --list
📋 可用的搜索引擎:
  • duckduckgo

💡 计划支持的搜索引擎:
  • google (开发中)
  • bing (开发中)
  • baidu (开发中)
```

## 技术栈

- **Python 3.13+**: 现代Python特性支持
- **Typer**: 强大的CLI框架，提供丰富的命令行功能
- **Poetry**: 现代Python依赖管理和打包工具
- **DuckDuckGo Search**: 免费的搜索API，无需API密钥
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
│   └── duckduckgo_search.md    # DuckDuckGo API文档
├── pyproject.toml              # Poetry配置和项目元数据
└── README.md                   # 项目文档
```

## 开发计划

- [x] 实现DuckDuckGo搜索引擎接口 ✅
- [x] 基础CLI命令框架 ✅  
- [x] 多种输出格式支持 (JSON, Table, Simple) ✅
- [x] 错误处理和用户提示 ✅
- [x] 完整的测试覆盖 ✅
- [ ] 实现Google搜索引擎接口
- [ ] 实现Bing搜索引擎接口  
- [ ] 实现Baidu搜索引擎接口
- [ ] 添加配置文件支持
- [ ] 实现结果缓存机制
- [ ] 添加搜索历史功能
- [ ] 支持搜索结果过滤和排序
- [ ] 添加更多输出格式（CSV、XML等）
- [ ] 添加代理支持
- [ ] 支持并行多引擎搜索

## 当前功能状态

### ✅ 已实现功能
- **DuckDuckGo 搜索**: 完整支持文本搜索
- **多种输出格式**: simple, json, table
- **CLI 参数**: --engine, --limit, --output, --verbose
- **错误处理**: 优雅的错误提示和帮助信息
- **测试覆盖**: 完整的单元测试和集成测试

### 🚧 开发中功能
- **配置文件**: 默认引擎设置 (基础框架已完成)
- **其他搜索引擎**: Google, Bing, Baidu (架构已就绪)

### 📋 计划功能
- **高级搜索**: 结果过滤、排序、缓存
- **批量操作**: 多查询、历史记录

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

## 许可证

MIT License
