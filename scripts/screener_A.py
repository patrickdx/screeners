import json
import os

# Example: Daily Gainers Screener
# This would normally fetch real data from an API like yfinance, Alpha Vantage, etc.

def get_daily_gainers():
    """
    Simulated screener for stocks with high daily gains.
    In production, replace this with actual API calls.
    """
    stock_data = [
        {"ticker": "AAPL", "change_pct": 5.2, "volume": 1200000},
        {"ticker": "MSFT", "change_pct": 4.1, "volume": 980000},
        {"ticker": "GOOGL", "change_pct": 3.8, "volume": 850000},
        {"ticker": "TSLA", "change_pct": 7.5, "volume": 2100000},
        {"ticker": "AMZN", "change_pct": 2.9, "volume": 750000}
    ]
    return stock_data

def main():
    print("Running Screener A: Daily Gainers...")
    
    # Get the screened data
    stock_data = get_daily_gainers()
    
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to JSON file
    output_path = "data/screener_A.json"
    with open(output_path, 'w') as f:
        json.dump({"data": stock_data}, f, indent=2)
    
    print(f"✓ Screener A complete. {len(stock_data)} stocks saved to {output_path}")

if __name__ == "__main__":
    main()
