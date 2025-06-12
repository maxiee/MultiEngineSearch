#!/bin/bash

# 多引擎搜索并保存结果的脚本
# 使用方法: ./mesobs.sh "搜索关键词"

KEYWORD="$1"
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
FILENAME="search_${TIMESTAMP}_$(echo "$KEYWORD" | tr ' ' '_').md"

# 假设的保存路径（从环境变量 MES_SAVE_PATH 读取，若未设置则使用默认路径）
SAVE_PATH="${MES_SAVE_PATH}"

# 创建目录
mkdir -p "$SAVE_PATH"

# 执行搜索并保存
echo "# 搜索结果: $KEYWORD" > "$SAVE_PATH/$FILENAME"
echo "" >> "$SAVE_PATH/$FILENAME"
echo "搜索时间: $(date)" >> "$SAVE_PATH/$FILENAME"
echo "" >> "$SAVE_PATH/$FILENAME"
mes search "$KEYWORD" >> "$SAVE_PATH/$FILENAME"

echo "搜索完成，结果保存到: $SAVE_PATH/$FILENAME"
