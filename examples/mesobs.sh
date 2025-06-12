#!/bin/bash

# 多引擎搜索并保存结果的脚本
# 使用方法: ./mesobs.sh "搜索关键词" [时间筛选]
# 时间筛选选项: d=最近一天, w=最近一周, m=最近一月, y=最近一年
# 如果不指定时间筛选，默认使用 y（最近一年）

KEYWORD="$1"
TIME_FILTER="${2:-y}"  # 第二个参数，如果为空则默认为 y（最近一年）

# 验证时间筛选参数
if [[ "$TIME_FILTER" != "d" && "$TIME_FILTER" != "w" && "$TIME_FILTER" != "m" && "$TIME_FILTER" != "y" ]]; then
    echo "❌ 无效的时间筛选参数: $TIME_FILTER"
    echo "支持的选项: d (一天), w (一周), m (一月), y (一年)"
    echo "使用方法: $0 \"搜索关键词\" [时间筛选]"
    echo "示例: $0 \"Python教程\" d"
    exit 1
fi

# 检查是否提供了搜索关键词
if [ -z "$KEYWORD" ]; then
    echo "❌ 请提供搜索关键词"
    echo "使用方法: $0 \"搜索关键词\" [时间筛选]"
    echo "时间筛选选项: d (一天), w (一周), m (一月), y (一年，默认)"
    echo "示例: $0 \"Python教程\" d"
    exit 1
fi

TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
FILENAME="search_${TIMESTAMP}_$(echo "$KEYWORD" | tr ' ' '_')_${TIME_FILTER}.md"

# 假设的保存路径（从环境变量 MES_SAVE_PATH 读取，若未设置则使用默认路径）
SAVE_PATH="${MES_SAVE_PATH}"

# 创建目录
mkdir -p "$SAVE_PATH"

# 时间筛选说明
declare -A TIME_LABELS
TIME_LABELS[d]="最近一天"
TIME_LABELS[w]="最近一周"
TIME_LABELS[m]="最近一月"
TIME_LABELS[y]="最近一年"

echo "🔍 正在搜索: $KEYWORD"
echo "⏰ 时间筛选: ${TIME_LABELS[$TIME_FILTER]}"
echo "📁 保存路径: $SAVE_PATH/$FILENAME"

# 执行搜索并保存
echo "# 搜索结果: $KEYWORD" > "$SAVE_PATH/$FILENAME"
echo "" >> "$SAVE_PATH/$FILENAME"
echo "搜索时间: $(date)" >> "$SAVE_PATH/$FILENAME"
echo "时间筛选: ${TIME_LABELS[$TIME_FILTER]}" >> "$SAVE_PATH/$FILENAME"
echo "" >> "$SAVE_PATH/$FILENAME"
mes search "$KEYWORD" --time "$TIME_FILTER" >> "$SAVE_PATH/$FILENAME"

echo "✅ 搜索完成，结果保存到: $SAVE_PATH/$FILENAME"
