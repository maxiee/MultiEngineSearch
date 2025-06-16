#!/bin/bash

# 多引擎搜索并保存结果的脚本
# 使用方法: ./mesobs.sh "搜索关键词" [搜索引擎] [时间筛选]
# 搜索引擎选项: google, duckduckgo (默认)
# 时间筛选选项: d=最近一天, w=最近一周, m=最近一月, y=最近一年
# 如果不指定时间筛选，默认使用 y（最近一年）

# 显示帮助信息
show_help() {
    echo "🔍 Multi-Engine Search 保存脚本 (mesobs)"
    echo ""
    echo "用法:"
    echo "  $0 \"搜索关键词\" [搜索引擎] [时间筛选]"
    echo "  $0 --help                                    # 显示帮助信息"
    echo ""
    echo "参数说明:"
    echo "  搜索关键词    必需参数，搜索的内容"
    echo "  搜索引擎      可选，支持: google, duckduckgo (默认: duckduckgo)"
    echo "  时间筛选      可选，支持: d(天), w(周), m(月), y(年) (默认: y)"
    echo ""
    echo "示例:"
    echo "  $0 \"Python教程\"                    # 使用默认引擎和时间筛选"
    echo "  $0 \"Python教程\" google             # 使用 Google 搜索"
    echo "  $0 \"Python教程\" duckduckgo d       # 使用 DuckDuckGo 搜索最近一天"
    echo "  $0 \"机器学习\" google m             # 使用 Google 搜索最近一月"
    echo ""
    echo "环境变量:"
    echo "  MES_SAVE_PATH    设置搜索结果保存路径 (默认: 当前目录)"
    echo ""
    echo "输出文件:"
    echo "  文件名格式: search_时间戳_关键词_引擎_时间筛选.md"
}

# 检查是否请求帮助
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi

KEYWORD="$1"
ENGINE="${2:-duckduckgo}"  # 第二个参数，如果为空则默认为 duckduckgo
TIME_FILTER="${3:-y}"      # 第三个参数，如果为空则默认为 y（最近一年）

# 验证搜索引擎参数
if [[ "$ENGINE" != "google" && "$ENGINE" != "duckduckgo" ]]; then
    echo "❌ 不支持的搜索引擎: $ENGINE"
    echo "支持的引擎: google, duckduckgo"
    echo "使用方法: $0 \"搜索关键词\" [搜索引擎] [时间筛选]"
    echo "示例: $0 \"Python教程\" google d"
    exit 1
fi

# 验证时间筛选参数
if [[ "$TIME_FILTER" != "d" && "$TIME_FILTER" != "w" && "$TIME_FILTER" != "m" && "$TIME_FILTER" != "y" ]]; then
    echo "❌ 无效的时间筛选参数: $TIME_FILTER"
    echo "支持的选项: d (一天), w (一周), m (一月), y (一年)"
    echo "使用方法: $0 \"搜索关键词\" [搜索引擎] [时间筛选]"
    echo "示例: $0 \"Python教程\" google d"
    exit 1
fi

# 检查是否提供了搜索关键词
if [ -z "$KEYWORD" ]; then
    echo "❌ 请提供搜索关键词"
    echo "使用方法: $0 \"搜索关键词\" [搜索引擎] [时间筛选]"
    echo "搜索引擎选项: google, duckduckgo (默认)"
    echo "时间筛选选项: d (一天), w (一周), m (一月), y (一年，默认)"
    echo ""
    echo "示例:"
    echo "  $0 \"Python教程\"                    # 使用默认引擎和时间筛选"
    echo "  $0 \"Python教程\" google             # 使用 Google 搜索"
    echo "  $0 \"Python教程\" duckduckgo d       # 使用 DuckDuckGo 搜索最近一天"
    echo "  $0 \"机器学习\" google m             # 使用 Google 搜索最近一月"
    exit 1
fi

TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
FILENAME="search_${TIMESTAMP}_$(echo "$KEYWORD" | tr ' ' '_')_${ENGINE}_${TIME_FILTER}.md"

# 假设的保存路径（从环境变量 MES_SAVE_PATH 读取，若未设置则使用当前目录）
SAVE_PATH="${MES_SAVE_PATH:-$(pwd)}"

# 创建目录
mkdir -p "$SAVE_PATH"

# 搜索引擎说明函数
get_engine_label() {
    case "$1" in
        "google") echo "Google" ;;
        "duckduckgo") echo "DuckDuckGo" ;;
        *) echo "未知引擎" ;;
    esac
}

# 时间筛选说明函数
get_time_label() {
    case "$1" in
        "d") echo "最近一天" ;;
        "w") echo "最近一周" ;;
        "m") echo "最近一月" ;;
        "y") echo "最近一年" ;;
        *) echo "未知" ;;
    esac
}

ENGINE_LABEL=$(get_engine_label "$ENGINE")
TIME_LABEL=$(get_time_label "$TIME_FILTER")

echo "🔍 正在搜索: $KEYWORD"
echo "🚀 搜索引擎: $ENGINE_LABEL"
echo "⏰ 时间筛选: $TIME_LABEL"
echo "📁 保存路径: $SAVE_PATH/$FILENAME"

# 执行搜索并保存
echo "# 搜索结果: $KEYWORD" > "$SAVE_PATH/$FILENAME"
echo "" >> "$SAVE_PATH/$FILENAME"
echo "搜索时间: $(date)" >> "$SAVE_PATH/$FILENAME"
echo "搜索引擎: $ENGINE_LABEL" >> "$SAVE_PATH/$FILENAME"
echo "时间筛选: $TIME_LABEL" >> "$SAVE_PATH/$FILENAME"
echo "" >> "$SAVE_PATH/$FILENAME"
mes search "$KEYWORD" --engine "$ENGINE" --time "$TIME_FILTER" >> "$SAVE_PATH/$FILENAME"

echo "✅ 搜索完成，结果保存到: $SAVE_PATH/$FILENAME"
