# Polymarket Data

<div align="center">

**High-performance toolkit for fetching and processing Polymarket on-chain data**

Fetch complete trading data directly from Polygon blockchain without relying on third-party data providers

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Features](#-features) • [Quick Start](#-quick-start) • [Dataset](#-dataset) • [Documentation](#-documentation)

</div>

---

## ✨ Features

- 🚀 **Direct RPC Access** - Fetch data directly from Polygon blockchain, no third-party dependencies
- 📊 **Complete Fields** - Get all fields including block_number, fees, order_hash that are missing in third-party data
- ⚡ **Real-time Continuous Mode** - Automatically follow latest blocks, sync new data every 2 seconds
- 🔄 **Resume from Checkpoint** - Auto-save progress, restart anytime without data loss
- 🧹 **Auto Data Cleaning** - Real-time generation of trades, quant, and users datasets
- 💾 **Efficient Storage** - Parquet format with compression, supports incremental writes
- 🎯 **Focused Design** - Only fetch OrderFilled events from two exchange contracts, minimal data overhead

## 🆚 vs Third-party Data Sources

| Field | polymarket-data | Third-party |
|-------|-----------------|-------------|
| block_number | ✅ | ❌ |
| contract (contract name) | ✅ | ❌ |
| maker_fee / taker_fee / protocol_fee | ✅ | ❌ |
| order_hash | ✅ | ❌ |
| market_id (auto-linked) | ✅ | ✅ |
| Missing token auto-fill | ✅ | ✅ |

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/polymarket-data.git
cd polymarket-data

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

### Usage

#### 1️⃣ Continuous Real-time Mode (Recommended)

Automatically fetch new blocks and keep running 24/7:

```bash
# Start continuous fetching
./scripts/continuous_start.sh

# View logs
tail -f logs/continuous_fetch.log

# Stop gracefully
./scripts/continuous_stop.sh
```

Features:
- **Batch mode**: When behind by ≥100 blocks, fetch 100 blocks at once
- **Real-time mode**: When caught up, fetch 1 block every 2 seconds
- **Auto data cleaning**: Generate 4 parquet files in real-time (orderfilled, trades, quant, users)
- **Graceful shutdown**: Ensures all files are properly closed on exit
- **New files per session**: Each run creates timestamped files (e.g., `orderfilled_20260101_120000.parquet`)

#### 2️⃣ Batch Historical Data

Fetch specific range of historical blocks:

```bash
# Fetch last 10,000 blocks
python -m polymarket.cli fetch-onchain --blocks 10000

# Resume from last checkpoint
python -m polymarket.cli fetch-onchain --continue

# Fetch specific block range
python -m polymarket.cli fetch-onchain --start 80000000 --end 80010000
```

#### 3️⃣ Full Pipeline

Complete workflow: fetch markets → fetch on-chain → process data:

```bash
# Run full pipeline
./scripts/update_all.sh

# Or step by step
./scripts/fetch_markets.sh        # Fetch market metadata
./scripts/fetch_onchain.sh 5000   # Fetch on-chain data (last 5000 blocks)
./scripts/clean_data.sh            # Clean and process data
```

#### 4️⃣ Python API

Use as a library in your Python code:

```python
from polymarket import LogFetcher, EventDecoder, extract_trades
from polymarket import load_token_mapping

# 1. Fetch on-chain logs
fetcher = LogFetcher()
logs = fetcher.fetch_range_in_batches(start_block, end_block)

# 2. Decode events
decoder = EventDecoder()
decoded = decoder.decode_batch(logs)
events = decoder.format_batch(decoded)

# 3. Load token mapping
token_mapping = load_token_mapping()

# 4. Extract trades (auto-link market_id)
trades_df = extract_trades(events, token_mapping)

# 5. Save to parquet
trades_df.to_parquet('trades.parquet')
```

## 📁 Project Structure

```
polymarket-data/
├── polymarket/              # Core Python package
│   ├── cli/                 # Command-line interface
│   ├── fetchers/            # Data fetchers (RPC, Gamma API)
│   ├── processors/          # Data processors (decoder, cleaner)
│   └── tools/               # Utility tools (merge, sort, etc.)
├── scripts/                 # Shell scripts for common tasks
├── data/                    # Data storage (gitignored)
├── logs/                    # Logs (gitignored)
├── README.md
├── LICENSE
└── requirements.txt
```

## 📊 Output Data Schema

### OrderFilled Events
Raw blockchain events with complete fields:

| Field | Description |
|-------|-------------|
| timestamp | Unix timestamp |
| datetime | Human-readable datetime |
| block_number | Block number |
| transaction_hash | Transaction hash |
| contract | Contract name (CTF_EXCHANGE or NEGRISK_CTF_EXCHANGE) |
| maker / taker | Trading parties' addresses |
| maker_asset_id / taker_asset_id | Asset IDs (uint256 as string) |
| maker_amount_filled / taker_amount_filled | Filled amounts |
| maker_fee / taker_fee / protocol_fee | Fees (in wei) |
| order_hash | Order hash |

### Trades
Processed trading data with market linkage:

| Field | Description |
|-------|-------------|
| market_id | Market ID (auto-linked from token) |
| answer | Option name (YES/NO/etc.) |
| token_id | Non-USDC token ID |
| nonusdc_side | Which side holds non-USDC token (maker/taker) |
| maker_direction / taker_direction | Buy/sell direction |
| price | Trade price (0-1) |
| usd_amount / token_amount | USDC and token amounts |

### Quant & Users
Additional datasets generated from trades for quantitative analysis and user behavior tracking.

## 🛠️ Utility Tools

All Python tools are available in `polymarket/tools/`:

```bash
# Merge multiple parquet files
python -m polymarket.tools.merge_parquet file1.parquet file2.parquet -o merged.parquet

# Sort parquet by timestamp
python -m polymarket.tools.sort_parquet input.parquet -o sorted.parquet

# Refetch failed blocks
python -m polymarket.tools.refetch_failed_blocks --start 80000000 --end 80100000
```

## 📦 Dataset

We provide complete historical data on HuggingFace:

🤗 **[polymarket-onchain-data](https://huggingface.co/datasets/yourusername/polymarket-onchain-data)** (Coming soon)

- Full historical OrderFilled events
- Processed trades data
- Quantitative and user datasets
- Updated daily

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Alchemy API key for faster RPC access
export ALCHEMY_API_KEY=your_key_here
```

### Custom RPC Endpoint

Edit `polymarket/config.py`:

```python
RPC_ENDPOINTS = [
    "https://polygon-rpc.com",
    "your_custom_endpoint",
]
```

## 📖 Documentation

### CLI Commands

```bash
# Fetch market metadata
python -m polymarket.cli fetch-markets

# Fetch on-chain data
python -m polymarket.cli fetch-onchain --blocks 1000
python -m polymarket.cli fetch-onchain --continue
python -m polymarket.cli fetch-onchain --start 80000000 --end 80010000

# Process data
python -m polymarket.cli process
python -m polymarket.cli process --skip-missing

# Full update
python -m polymarket.cli update
```

### Continuous Fetching Details

The continuous mode operates in two phases:

1. **Batch Mode** (when behind by ≥100 blocks)
   - Fetches 100 blocks per request
   - Fast catch-up to latest block
   - No sleep between requests

2. **Real-time Mode** (when caught up)
   - Fetches 1 block per request
   - 2-second sleep between requests (matches Polymarket block time)
   - Minimal RPC load

Each session creates new timestamped files:
- `orderfilled_20260101_120000.parquet`
- `trades_20260101_120000.parquet`
- `quant_20260101_120000.parquet`
- `users_20260101_120000.parquet`

Plus real-time CSV previews (latest 1000 records) in `data/latest_result/`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Polymarket for the amazing prediction market platform
- Polygon for the blockchain infrastructure
- The open-source community

## ⚠️ Disclaimer

This tool is for research and educational purposes. Users are responsible for complying with Polymarket's terms of service and applicable regulations.

---

<div align="center">
Made with ❤️ by the Polymarket Data community
</div>
