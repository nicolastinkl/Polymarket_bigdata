"""
02_market_overview.py - 市场概览和统计

分析 BTC/ETH/SOL 市场的分布、时间周期、交易量等基础统计信息。

运行方式:
    python 02_market_overview.py

依赖:
    pip install duckdb pandas
"""

import duckdb
import pandas as pd
import re

def classify_timeframe(question):
    """根据问题文本分类时间周期 (5m/15m/1h)"""
    match = re.search(r'(\d+:\d+[AP]M)-(\d+:\d+[AP]M)', question)
    if match:
        start, end = match.groups()
        
        def parse_time(t):
            h, rest = t.split(':')
            m = rest[:-2]
            ampm = rest[-2:]
            h, m = int(h), int(m)
            if ampm == 'PM' and h != 12: h += 12
            elif ampm == 'AM' and h == 12: h = 0
            return h * 60 + m
        
        dur = parse_time(end) - parse_time(start)
        if dur < 0: dur += 24 * 60
        
        if dur <= 5: return '5m'
        elif dur <= 15: return '15m'
        else: return 'other'
    elif re.search(r'\d+:\d+[AP]M ET$', question):
        return '1h'
    return 'daily'

def classify_crypto(question):
    """分类加密货币类型"""
    if 'BTC' in question or 'Bitcoin' in question: return 'BTC'
    elif 'ETH' in question or 'Ethereum' in question: return 'ETH'
    elif 'SOL' in question or 'Solana' in question: return 'SOL'
    return 'OTHER'

def main():
    con = duckdb.connect()
    
    print("=" * 100)
    print("📊 市场概览：BTC/ETH/SOL Up or Down 市场分析")
    print("=" * 100)
    
    # 1. 获取所有相关市场
    print("\n[1] 获取市场数据...")
    markets = con.execute("""
        SELECT id, question, outcome_prices, end_date, volume, closed, created_at
        FROM '../data/markets.parquet'
        WHERE (question ILIKE '%BTC%' OR question ILIKE '%Bitcoin%'
               OR question ILIKE '%ETH%' OR question ILIKE '%Ethereum%'
               OR question ILIKE '%SOL%' OR question ILIKE '%Solana%')
          AND (question ILIKE '%Up or Down%')
    """).fetchdf()
    
    markets['crypto'] = markets['question'].apply(classify_crypto)
    markets['timeframe'] = markets['question'].apply(classify_timeframe)
    markets['month'] = pd.to_datetime(markets['end_date']).dt.to_period('M')
    
    print(f"总市场数: {len(markets):,}")
    
    # 2. 按加密货币分布
    print("\n[2] 按加密货币分布:")
    print("-" * 60)
    crypto_dist = markets['crypto'].value_counts()
    for crypto, count in crypto_dist.items():
        pct = count / len(markets) * 100
        print(f"  {crypto}: {count:,} ({pct:.1f}%)")
    
    # 3. 按时间周期分布
    print("\n[3] 按时间周期分布:")
    print("-" * 60)
    tf_dist = markets['timeframe'].value_counts()
    for tf, count in tf_dist.items():
        pct = count / len(markets) * 100
        print(f"  {tf}: {count:,} ({pct:.1f}%)")
    
    # 4. 按月份统计
    print("\n[4] 按月份统计 (最近 6 个月):")
    print("-" * 60)
    monthly = markets.groupby('month').agg(
        markets=('id', 'count'),
        total_volume=('volume', 'sum'),
        avg_volume=('volume', 'mean')
    ).tail(6)
    
    print(f"{'月份':<10} {'市场数':>8} {'总交易量$':>15} {'平均$':>12}")
    print("-" * 50)
    for month, row in monthly.iterrows():
        print(f"{str(month):<10} {int(row['markets']):>8,} ${row['total_volume']:>13,.0f} ${row['avg_volume']:>10,.0f}")
    
    # 5. BTC 5m 市场深度分析
    print("\n[5] BTC 5m 市场深度分析:")
    print("-" * 60)
    
    btc_5m = markets[(markets['crypto'] == 'BTC') & (markets['timeframe'] == '5m')]
    settled = btc_5m[btc_5m['closed'] == 1]
    
    print(f"总市场数: {len(btc_5m):,}")
    print(f"已结算: {len(settled):,}")
    print(f"UP 赢: {(settled['outcome_prices'] == \"['1', '0']\").sum():,}")
    print(f"DOWN 赢: {(settled['outcome_prices'] == \"['0', '1']\").sum():,}")
    print(f"总交易量: ${settled['volume'].sum():,.0f}")
    print(f"平均交易量: ${settled['volume'].mean():,.0f}")
    
    # 6. UP/DOWN 胜率统计
    print("\n[6] UP/DOWN 胜率统计:")
    print("-" * 60)
    
    for crypto in ['BTC', 'ETH', 'SOL']:
        c_markets = markets[markets['crypto'] == crypto]
        c_settled = c_markets[c_markets['closed'] == 1]
        
        up_wins = (c_settled['outcome_prices'] == "['1', '0']").sum()
        down_wins = (c_settled['outcome_prices'] == "['0', '1']").sum()
        total = up_wins + down_wins
        
        up_rate = up_wins / total * 100 if total > 0 else 0
        
        print(f"\n{crypto}:")
        print(f"  UP 赢: {up_wins:,} ({up_rate:.1f}%)")
        print(f"  DOWN 赢: {down_wins:,} ({100-up_rate:.1f}%)")
        print(f"  总计: {total:,}")
    
    print("\n\n✅ 市场概览完成")


if __name__ == "__main__":
    main()
