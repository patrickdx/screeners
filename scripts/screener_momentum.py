"""
Momentum Screener - Automated Version
Finds stocks breaking out to new highs with strong relative strength
Outputs: data/screener_momentum.json
"""

import pandas as pd
import yfinance as yf
import datetime
import os
import json
import time

# ---------- CONFIG ----------
SOFT_BREAKOUT_PCT = 0.15  # 15% from high
PROXIMITY_THRESHOLD = 0.05  # 5% from high
VOLUME_THRESHOLD = 1.0  # % above average volume
LOOKBACK_DAYS = 365
SKIP_RECENT_DAYS = 0
BATCH_SIZE = 101            # Number of tickers per batch download
SLEEP_BETWEEN_BATCHES = 1   # Pause between each batch download


def get_sp500_tickers():
    """Fetch S&P 500 ticker list from Wikipedia"""
    sp500_tables = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
        storage_options={"User-Agent": "Mozilla/5.0"}
    )
    
    for table in sp500_tables:
        if 'Symbol' in table.columns:
            return table['Symbol'].tolist()
    
    raise ValueError("Could not find the S&P 500 table")


def download_batch_with_retry(tickers, start, end, retries=3, sleep_time=2):
    """Download data with retry logic"""
    attempt = 0
    while attempt < retries:
        try:
            data = yf.download(
                tickers, 
                start=start, 
                end=end, 
                group_by="ticker", 
                auto_adjust=True, 
                progress=False, 
                threads=True
            )
            return data
        except Exception as e:
            attempt += 1
            print(f"  Error downloading batch (attempt {attempt}/{retries}): {e}")
            time.sleep(sleep_time)
    return None


def download_all_in_batches(ticker_list, start_date, end_date, batch_size=50, sleep_time=2):
    """Download all tickers in batches"""
    all_data = {}
    failed_batches = []
    
    print("\nDownloading data in batches...")
    for i in range(0, len(ticker_list), batch_size):
        batch = ticker_list[i:i + batch_size]
        print(f"Batch {i // batch_size + 1}: {batch[0]} to {batch[-1]}")
        
        data = download_batch_with_retry(batch, start_date, end_date)
        
        if data is None or data.empty:
            failed_batches.extend(batch)
        else:
            for ticker in batch:
                if ticker in data.columns.get_level_values(0):
                    all_data[ticker] = data[ticker]
                else:
                    failed_batches.append(ticker)
        
        time.sleep(sleep_time)
    
    return all_data, failed_batches


def calculate_momentum_screener():
    """Main screener logic"""
    print("Running Momentum Screener...")
    
    # Get universe
    universe = get_sp500_tickers()
    universe = [ticker.replace('.', '-') for ticker in universe]
    
    if 'SPY' not in universe:
        universe.append('SPY')
    
    print(f"Universe: S&P 500 ({len(universe)} tickers)")
    
    # Download data
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=LOOKBACK_DAYS)
    
    raw_data, failed_tickers = download_all_in_batches(
        universe, 
        start_date, 
        end_date,
        batch_size=BATCH_SIZE,
        sleep_time=SLEEP_BETWEEN_BATCHES
    )
    
    if not raw_data:
        raise RuntimeError("No data downloaded")
    
    data = pd.concat(raw_data, axis=1)
    
    # Calculate metrics
    close_prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in raw_data})
    high_prices = pd.DataFrame({ticker: data[ticker]['High'] for ticker in raw_data})
    volume_dict = {ticker: data[(ticker, 'Volume')] for ticker in raw_data}
    avg_vol_50_dict = {ticker: vol.rolling(50).mean() for ticker, vol in volume_dict.items()}
    
    current_close = close_prices.iloc[-1]
    rolling_high = high_prices.rolling(LOOKBACK_DAYS, min_periods=1).max()
    rolling_high_today = rolling_high.iloc[-1]
    latest_volume = pd.Series({ticker: vol.iloc[-1] for ticker, vol in volume_dict.items()})
    latest_avg_volume = pd.Series({ticker: avg.iloc[-1] for ticker, avg in avg_vol_50_dict.items()})
    volume_ratio = latest_volume / latest_avg_volume
    proximity = (rolling_high_today - current_close) / rolling_high_today
    
    # Relative Strength
    relative_strength = close_prices.div(close_prices['SPY'], axis=0)
    
    if SKIP_RECENT_DAYS == 0:
        RS_momentum = (relative_strength.iloc[-1] / relative_strength.iloc[0]) - 1
    else:
        RS_momentum = (relative_strength.iloc[-SKIP_RECENT_DAYS] / relative_strength.iloc[0]) - 1
    
    RS_momentum = RS_momentum.drop('SPY', errors='ignore')
    
    # Breakout Logic: if proximity within threshold SOFT_BREAKOUT_PCT and volume ratio above threshold VOLUME_THRESHOLD
    high_breakers = (proximity <= SOFT_BREAKOUT_PCT) & (volume_ratio > VOLUME_THRESHOLD)
    
    # Build DataFrame
    breakout_df = pd.DataFrame({
        "ticker": current_close[high_breakers].index,
        "price": current_close[high_breakers].values,
        "high_52w": rolling_high_today[high_breakers].values,
        "dist_to_high_pct": (proximity[high_breakers] * 100).values,
        "volume_ratio": volume_ratio[high_breakers].values,
        "rs_score": RS_momentum[high_breakers].values,
    }).dropna().sort_values(by="dist_to_high_pct")
    
    # Round values
    breakout_df['price'] = breakout_df['price'].round(2)
    breakout_df['high_52w'] = breakout_df['high_52w'].round(2)
    breakout_df['dist_to_high_pct'] = breakout_df['dist_to_high_pct'].round(2)
    breakout_df['volume_ratio'] = breakout_df['volume_ratio'].round(2)
    breakout_df['rs_score'] = breakout_df['rs_score'].round(2)
    
    return breakout_df


def main():
    """Main execution"""
    try:
        # Run screener
        results_df = calculate_momentum_screener()
        
        # Convert to list of dicts for JSON
        results_list = results_df.to_dict('records')
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save to JSON
        output_path = "data/screener_momentum.json"
        with open(output_path, 'w') as f:
            json.dump({"data": results_list}, f, indent=2)
        
        print(f"✓ Momentum Screener complete. {len(results_list)} stocks saved to {output_path}")
        
    except Exception as e:
        print(f"❌ Error in momentum screener: {e}")
        # Save empty data so the frontend doesn't break
        os.makedirs("data", exist_ok=True)
        with open("data/screener_momentum.json", 'w') as f:
            json.dump({"data": []}, f)


if __name__ == "__main__":
    main()
