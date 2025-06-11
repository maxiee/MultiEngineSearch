# MultiEngineSearch (mse)

一个遵循Unix哲学原则的多搜索引擎统一命令行界面工具。

## 概述

MultiEngineSearch (mse) 是一个轻量级、可扩展的命令行工具，提供了查询多个搜索引擎的统一接口。它专注于做好一件事：通过一致的输出格式和灵活的配置选项在不同引擎间进行搜索。

## 特性

- **多搜索引擎支持**: 查询 Google、Bing、DuckDuckGo 和其他流行搜索引擎
- **灵活的输出格式**: 支持 JSON、Markdown 或纯文本格式导出结果
- **Unix友好**: 支持管道、重定向，遵循Unix约定
- **可配置**: 易于使用的配置文件管理API密钥和偏好设置
- **可扩展**: 插件架构，便于添加新的搜索引擎
- **轻量级**: 最小依赖，快速执行

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
# 基本搜索
mse search "python编程教程"

# 使用特定搜索引擎
mse search "机器学习基础" --engine google

# 输出为JSON格式
mse search "网页开发" --output json --limit 5

# 显示详细信息
mse search "气候变化" --verbose --engine google --limit 10
```

## 使用方法

### 搜索命令

```bash
mse search [查询内容] [选项]
```

**选项:**
- `--engine, -e`: 指定搜索引擎 (google, bing, duckduckgo, baidu)
- `--limit, -l`: 返回结果数量限制 (1-100，默认10)
- `--output, -o`: 输出格式 (json, table, simple，默认simple)
- `--verbose, -v`: 显示详细信息

**示例:**
```bash
# 基本搜索
mse search "Python教程"

# 指定引擎和结果数量
mse search "机器学习" --engine google --limit 5

# JSON格式输出
mse search "AI新闻" --output json --verbose
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

# 设置默认引擎
mse config --set-default google
```

### 版本信息

```bash
# 显示版本信息
mse version
```

## 技术栈

- **Python 3.13+**: 现代Python特性支持
- **Typer**: 强大的CLI框架，提供丰富的命令行功能
- **Poetry**: 现代Python依赖管理和打包工具
- **Rich**: 美观的终端输出和格式化

## 项目结构

```
MultiEngineSearch/
├── src/
│   └── multienginesearch/
│       ├── __init__.py          # 包初始化
│       └── cli.py               # CLI入口和命令定义
├── tests/                       # 测试文件
├── pyproject.toml              # Poetry配置和项目元数据
└── README.md                   # 项目文档
```

## 开发计划

- [ ] 实现Google搜索引擎接口
- [ ] 实现Bing搜索引擎接口  
- [ ] 实现DuckDuckGo搜索引擎接口
- [ ] 添加配置文件支持
- [ ] 实现结果缓存机制
- [ ] 添加搜索历史功能
- [ ] 支持搜索结果过滤和排序
- [ ] 添加更多输出格式（CSV、XML等）

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

## 许可证

MIT License
