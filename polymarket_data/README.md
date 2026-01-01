<div align="center">

# Polymarket Data

<h3>Complete Data Infrastructure for Polymarket — Fetch, Process, Analyze</h3>

<p>
A comprehensive dataset of 1.1 billion trading records from Polymarket, processed into multiple analysis-ready formats. Features cleaned data, unified token perspectives, and user-level transformations — ready for market research, behavioral studies, and quantitative analysis.
</p>

<p>
<b>Zhengjie Wang</b><sup>1,2</sup>, <b>Leiyu Chao</b><sup>2,3</sup>, <b>Yikang Li</b><sup>2,†</sup>
</p>

<p>
<sup>1</sup>Westlake University &nbsp;&nbsp; <sup>2</sup>Shanghai Innovation Institute &nbsp;&nbsp; <sup>3</sup>Shanghai Jiao Tong University
</p>

<p>
<sup>†</sup>Corresponding author
</p>

</div>

<p align="center">
  <a href="https://huggingface.co/datasets/SII-WANGZJ/Polymarket_data">
    <img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-yellow.svg" alt="HuggingFace Dataset"/>
  </a>
  <a href="https://github.com/SII-WANGZJ/Polymarket_data">
    <img src="https://img.shields.io/badge/GitHub-Code-black.svg?logo=github" alt="GitHub Repository"/>
  </a>
  <a href="https://github.com/SII-WANGZJ/Polymarket_data/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"/>
  </a>
  <a href="#data-quality">
    <img src="https://img.shields.io/badge/Data-Verified-green.svg" alt="Data Quality"/>
  </a>
</p>

---

## 🌟 TL;DR

We provide **107GB of historical on-chain trading data** from Polymarket, containing **1.1 billion records** across 268K+ markets. The dataset is directly fetched from Polygon blockchain, fully verified, and ready for analysis. Perfect for market research, behavioral studies, data science projects, and academic research.

## 🌱 Highlights

- **📊 Complete Blockchain History**: All OrderFilled events from Polymarket's two exchange contracts, with no missing blocks or gaps. Every single trade from the platform's inception is included.

- **🎯 Multiple Analysis Perspectives**: 5 carefully curated datasets serving different research needs - from raw blockchain events to user-level behavior analysis, with unified data transformations for easy analysis.

- **✅ Production Ready**: Clean, validated data with proper schema documentation. All trades are verified against blockchain RPC, with market metadata linked and ready to use.

- **🔄 Open Source Pipeline**: Fully reproducible data collection process. Our open-source tools allow you to verify, update, or extend the dataset independently.

## 📦 Dataset Overview

| File | Size | Records | Description |
|------|------|---------|-------------|
| `orderfilled.parquet` | 31GB | 293.3M | Raw blockchain events from OrderFilled logs |
| `trades.parquet` | 32GB | 293.3M | Processed trades with market metadata linkage |
| `markets.parquet` | 68MB | 268,706 | Market information and metadata |
| `quant.parquet` | 21GB | 170.3M | Clean market data with unified YES perspective |
| `users.parquet` | 23GB | 340.6M | User behavior data split by maker/taker roles |

**Total**: 107GB, 1.1 billion records

## 🎯 Use Cases

### Market Research & Analysis
- Study prediction market dynamics and price discovery mechanisms
- Analyze market efficiency and information aggregation
- Research crowd wisdom and forecasting accuracy

### Behavioral Studies
- Track individual user trading patterns and decision-making
- Study market participant behavior under different conditions
- Analyze risk preferences and trading strategies

### Data Science & Machine Learning
- Train models for price prediction and market forecasting
- Feature engineering for time-series analysis
- Develop algorithms for market analysis

### Academic Research
- Economics and finance research on prediction markets
- Social science studies on collective intelligence
- Computer science research on blockchain data analysis

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install pandas pyarrow

# Optional: for faster parquet reading
pip install fastparquet
```

### Load Data with Pandas

```python
import pandas as pd

# Load clean market data
df = pd.read_parquet('quant.parquet')
print(f"Total trades: {len(df):,}")

# Load user behavior data
users = pd.read_parquet('users.parquet')
print(f"Total user actions: {len(users):,}")

# Load market metadata
markets = pd.read_parquet('markets.parquet')
print(f"Total markets: {len(markets):,}")
```

### Load from HuggingFace Datasets

```python
from datasets import load_dataset

# Load specific file
dataset = load_dataset(
    "SII-WANGZJ/Polymarket_data",
    data_files="quant.parquet"
)

# Load multiple files
dataset = load_dataset(
    "SII-WANGZJ/Polymarket_data",
    data_files=["quant.parquet", "markets.parquet"]
)
```

### Download Specific Files

```bash
# Download using HuggingFace CLI
pip install huggingface_hub

# Download a specific file
hf download SII-WANGZJ/Polymarket_data quant.parquet --repo-type dataset

# Download all files
hf download SII-WANGZJ/Polymarket_data --repo-type dataset
```

## 📊 Data Structure

### quant.parquet - Clean Market Data

Filtered and normalized trade data with unified token perspective (YES token).

**Key Features:**
- ✅ Unified perspective: All trades normalized to YES token (token1)
- ✅ Clean data: Contract trades filtered out, only real user trades
- ✅ Complete information: Maker/taker roles preserved
- 📊 Best for: Market analysis, price studies, time-series forecasting

**Schema:**
```python
{
    'transaction_hash': str,      # Blockchain transaction hash
    'block_number': int,          # Block number
    'datetime': datetime,         # Transaction timestamp
    'market_id': str,             # Market identifier
    'maker': str,                 # Maker wallet address
    'taker': str,                 # Taker wallet address
    'token_amount': float,        # Amount of tokens traded
    'usd_amount': float,          # USD value
    'price': float,               # Trade price (0-1)
}
```

### users.parquet - User Behavior Data

Split maker/taker records with unified buy direction for user analysis.

**Key Features:**
- ✅ Split records: Each trade becomes 2 records (one maker, one taker)
- ✅ Unified direction: All converted to BUY (negative amounts = selling)
- ✅ User sorted: Ordered by user for trajectory analysis
- 👤 Best for: User profiling, PnL calculation, wallet analysis

**Schema:**
```python
{
    'transaction_hash': str,      # Transaction hash
    'block_number': int,          # Block number
    'datetime': datetime,         # Timestamp
    'market_id': str,             # Market identifier
    'user': str,                  # User wallet address
    'role': str,                  # 'maker' or 'taker'
    'token_amount': float,        # Signed amount (+ buy, - sell)
    'usd_amount': float,          # USD value
    'price': float,               # Trade price
}
```

### markets.parquet - Market Metadata

Market information and outcome token details.

**Best for:** Linking trades to market context, filtering by market attributes

### trades.parquet - Processed Blockchain Data

Raw OrderFilled events with market linkage but no transformations.

**Best for:** Custom analysis requiring original blockchain data

### orderfilled.parquet - Raw Blockchain Events

Unprocessed OrderFilled events directly from blockchain logs.

**Best for:** Blockchain research, verification, custom processing pipelines

## 💡 Example Analysis

### 1. Calculate Market Statistics

```python
import pandas as pd

df = pd.read_parquet('quant.parquet')

# Market-level statistics
market_stats = df.groupby('market_id').agg({
    'usd_amount': ['sum', 'mean'],     # Total volume and average trade size
    'price': ['mean', 'std', 'min', 'max'],  # Price statistics
    'transaction_hash': 'count'         # Number of trades
}).round(4)

print(market_stats.head())
```

### 2. Track Price Evolution

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet('quant.parquet')
df['datetime'] = pd.to_datetime(df['datetime'])

# Select a specific market
market_id = 'your-market-id'
market_data = df[df['market_id'] == market_id].sort_values('datetime')

# Plot price over time
plt.figure(figsize=(12, 6))
plt.plot(market_data['datetime'], market_data['price'])
plt.title(f'Price Evolution - Market {market_id}')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
```

### 3. Analyze User Behavior

```python
import pandas as pd

df = pd.read_parquet('users.parquet')

# Calculate net position per user per market
user_positions = df.groupby(['user', 'market_id']).agg({
    'token_amount': 'sum',          # Net position (positive = long, negative = short)
    'usd_amount': 'sum',            # Total USD traded
    'transaction_hash': 'count'     # Number of trades
}).reset_index()

# Find most active users
active_users = user_positions.groupby('user').agg({
    'market_id': 'count',           # Number of markets traded
    'usd_amount': 'sum'             # Total volume
}).sort_values('usd_amount', ascending=False)

print(active_users.head(10))
```

### 4. Market Volume Analysis

```python
import pandas as pd

df = pd.read_parquet('quant.parquet')
markets = pd.read_parquet('markets.parquet')

# Join with market metadata
df = df.merge(markets[['market_id', 'question']], on='market_id', how='left')

# Top markets by volume
top_markets = df.groupby(['market_id', 'question']).agg({
    'usd_amount': 'sum'
}).sort_values('usd_amount', ascending=False).head(20)

print(top_markets)
```

## 🔄 Data Processing Pipeline

```
Polygon Blockchain (RPC)
         ↓
  orderfilled.parquet (Raw events)
         ↓
  trades.parquet (+ Market linkage)
         ↓
         ├─→ quant.parquet (Trade-level, unified YES perspective)
         │   └─→ Filter contracts + Normalize tokens
         │
         └─→ users.parquet (User-level, split maker/taker)
             └─→ Split records + Unified BUY direction
```

**Key Transformations:**

1. **quant.parquet**:
   - Filter out contract trades (keep only user trades)
   - Normalize all trades to YES token perspective
   - Preserve maker/taker information
   - Result: 170.3M records (from 293.3M)

2. **users.parquet**:
   - Split each trade into 2 records (maker + taker)
   - Convert all to BUY direction (signed amounts)
   - Sort by user for easy querying
   - Result: 340.6M records (from 293.3M × 2, some filtered)

## 📖 Documentation

- **[DATA_DESCRIPTION.md](DATA_DESCRIPTION.md)** - Comprehensive documentation
  - Detailed schema for all 5 files
  - Data cleaning and transformation process
  - Usage examples and best practices
  - Comparison between different files

## 📊 Data Quality

- ✅ **Complete History**: No missing blocks or gaps in blockchain data
- ✅ **Verified Sources**: All OrderFilled events from 2 official exchange contracts
- ✅ **Blockchain Verified**: Cross-checked against Polygon RPC nodes
- ✅ **Regular Updates**: Automated daily pipeline for fresh data
- ✅ **Open Source**: Fully reproducible collection process

**Contracts Tracked:**
- Exchange Contract 1: `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`
- Exchange Contract 2: `0xC5d563A36AE78145C45a50134d48A1215220f80a`

## 🛠️ Collection Tools

Data collected using our open-source toolkit: [polymarket-data](https://github.com/SII-WANGZJ/Polymarket_data)

**Features:**
- Direct blockchain RPC integration
- Efficient batch processing
- Automatic retry and error handling
- Data validation and verification

## 📈 Dataset Statistics

**Last Updated**: 2026-01-01

**Coverage**:
- Time Range: [Polymarket inception] to [Latest update]
- Total Markets: 268,706
- Total Trades: 293.3 million
- Total Volume: $[To be calculated] billion
- Unique Users: [To be calculated]

**Data Freshness**: Updated daily via automated pipeline

## 🤝 Contributing

We welcome contributions to improve the dataset and tools:

1. **Report Issues**: Found data quality issues? [Open an issue](https://github.com/SII-WANGZJ/Polymarket_data/issues)
2. **Suggest Features**: Ideas for new data transformations? Let us know!
3. **Contribute Code**: Improve our collection pipeline via pull requests

## ⚖️ License

MIT License - Free for commercial and research use.

See [LICENSE](LICENSE) file for details.

## 📞 Contact & Support

- **Email**: [wangzhengjie@sii.edu.cn](mailto:wangzhengjie@sii.edu.cn)
- **Issues**: [GitHub Issues](https://github.com/SII-WANGZJ/Polymarket_data/issues)
- **Dataset**: [HuggingFace](https://huggingface.co/datasets/SII-WANGZJ/Polymarket_data)
- **Code**: [GitHub Repository](https://github.com/SII-WANGZJ/Polymarket_data)

## 📚 Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{polymarket_data_2025,
  title={Polymarket Data: Complete Data Infrastructure for Polymarket},
  author={Wang, Zhengjie and Chao, Leiyu and Li, Yikang},
  year={2025},
  institution={Shanghai Innovation Institute},
  url={https://huggingface.co/datasets/SII-WANGZJ/Polymarket_data},
  note={A comprehensive dataset and toolkit for Polymarket prediction markets}
}
```

## 🙏 Acknowledgments

- **Polymarket** for building the leading prediction market platform
- **Polygon** for providing reliable blockchain infrastructure
- **HuggingFace** for hosting and distributing large datasets
- The open-source community for tools and libraries

---

<div align="center">

**Built with ❤️ for the research and data science community**

[HuggingFace](https://huggingface.co/datasets/SII-WANGZJ/Polymarket_data) • [GitHub](https://github.com/SII-WANGZJ/Polymarket_data) • [Documentation](DATA_DESCRIPTION.md)

</div>
