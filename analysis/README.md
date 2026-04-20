# Polymarket 数据分析项目

这是一个针对 Polymarket BTC/ETH/SOL 预测市场的深度数据分析项目。基于 100GB+ 的链上交易数据（11 亿条记录），我们对市场微观结构、投注行为模式和潜在策略进行了系统性研究。

## 📊 数据集概览

| 文件 | 大小 | 记录数 | 说明 |
|------|------|--------|------|
| `markets.parquet` | 116MB | 734K | 市场元数据 |
| `quant.parquet` | 36GB | 5.68 亿 | 量化交易数据 |
| `users.parquet` | 48GB | 数据清洗后的用户行为 |

## 📁 分析脚本

按顺序运行以下脚本（每个脚本独立运行）：

```bash
cd analysis/

# 1. 数据验证：确认字段含义和数据完整性
python 01_data_validation.py

# 2. 市场概览：BTC/ETH/SOL 市场统计
python 02_market_overview.py

# 3. 秒级价格监控：价格时间序列分析
python 03_second_level_price.py

# 4. 投注行为分析：大户/散户行为模式
python 04_betting_behavior.py

# 5. 策略回测：期望值和盈亏分析
python 05_strategy_backtest.py
```

## 🔑 核心发现

### 1. 数据字段含义
- `price`: **UP token 的价格** (0-1 之间)
- `outcome_prices = ['1','0']`: UP=1, Down=0 → **UP 赢**
- `outcome_prices = ['0','1']`: UP=0, Down=1 → **DOWN 赢**
- UP 赢 → 价格趋近 1.0；DOWN 赢 → 价格趋近 0.0

### 2. 市场定价效率
- 市场定价非常有效，最大偏差仅 **2.2%**
- 不存在系统性套利机会
- 手续费 (约 2%) 吃掉了所有潜在利润

### 3. 投注行为模式
- **大户**偏好提前 3-5 分钟建仓（单笔 $3K-6K）
- **散户**集中在最后 10 秒涌入（单笔 $6-30）
- 95-100¢ 区间交易量最大（$195M），UP 方向主导

### 4. 策略回测结论
- **95¢ 买 UP 策略**：
  - 无手续费：期望值 +2.42%/Token ✅
  - 2% 手续费：期望值 -1.63%/Token ❌
- **结论**：对散户（Taker，2% 费）来说长期必亏

## 🛠 技术栈

- **DuckDB**: 高效 Parquet 文件查询（避免 Pandas 内存溢出）
- **Python 3.12+**: 主要编程语言
- **Pandas**: 数据处理和聚合
- **PyArrow**: Parquet 文件格式支持

## ⚠️ 免责声明

本项目仅用于**学术研究和教育目的**。所有分析结果不构成任何投资建议。预测市场交易存在风险，过往表现不代表未来结果。

## 📄 License

MIT License
