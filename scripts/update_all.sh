#!/bin/bash
# Full update: fetch markets, on-chain data, and process
# 修复版：增加错误处理和路径检查

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Full Update Pipeline ===${NC}"
echo ""

# 检查 Python 环境
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python${NC}"
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)
echo "使用 Python: $PYTHON"
echo ""

# 检查数据目录符号链接
echo "[0/4] 检查数据目录..."
if [ ! -L "polymarket/data/dataset/markets.parquet" ]; then
    echo -e "${YELLOW}警告: 符号链接不存在，正在创建...${NC}"
    mkdir -p polymarket/data/dataset
    ln -sf $(pwd)/data/markets.parquet polymarket/data/dataset/markets.parquet
    ln -sf $(pwd)/data/quant.parquet polymarket/data/dataset/quant.parquet
    ln -sf $(pwd)/data/users.parquet polymarket/data/dataset/users.parquet
    ln -sf $(pwd)/data/state.json polymarket/data/state.json
    echo -e "${GREEN}✓ 符号链接创建完成${NC}"
fi
echo ""

echo "[1/4] Fetching market data..."
if $PYTHON -m polymarket.cli fetch-markets; then
    echo -e "${GREEN}✓ 市场数据获取成功${NC}"
else
    echo -e "${RED}✗ 市场数据获取失败${NC}"
    exit 1
fi
echo ""

echo "[2/4] Fetching on-chain data..."
if $PYTHON -m polymarket.cli fetch-onchain --continue; then
    echo -e "${GREEN}✓ 链上数据获取成功${NC}"
else
    echo -e "${RED}✗ 链上数据获取失败${NC}"
    exit 1
fi
echo ""

echo "[3/4] Processing data..."
if $PYTHON -m polymarket.cli process; then
    echo -e "${GREEN}✓ 数据处理成功${NC}"
else
    echo -e "${RED}✗ 数据处理失败${NC}"
    exit 1
fi
echo ""

echo "[4/4] Verifying data integrity..."
if [ -f "polymarket/data/dataset/markets.parquet" ] && [ -f "polymarket/data/dataset/trades.parquet" ]; then
    echo -e "${GREEN}✓ 数据文件验证通过${NC}"
else
    echo -e "${YELLOW}⚠ 部分数据文件可能缺失${NC}"
fi
echo ""

echo -e "${GREEN}=== Full update completed successfully ===${NC}"
