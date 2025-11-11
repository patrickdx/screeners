import json
import os

# Example: Oversold Signals Screener (RSI-based)
# This would normally fetch real data from an API with technical indicators

def get_oversold_signals():
    """
    Simulated screener for oversold stocks based on RSI.
    In production, replace this with actual API calls and calculations.
    """
    stock_data = [
        {"ticker": "NVDA", "rsi": 28.5, "signal": "Buy"},
        {"ticker": "AMD", "rsi": 29.2, "signal": "Buy"},
        {"ticker": "INTC", "rsi": 25.8, "signal": "Strong Buy"},
        {"ticker": "MU", "rsi": 31.0, "signal": "Buy"},
        {"ticker": "QCOM", "rsi": 27.3, "signal": "Buy"}
    ]
    return stock_data

def main():
    print("Running Screener B: Oversold Signals...")
    
    # Get the screened data
    stock_data = get_oversold_signals()
    
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to JSON file
    output_path = "data/screener_B.json"
    with open(output_path, 'w') as f:
        json.dump({"data": stock_data}, f, indent=2)
    
    print(f"✓ Screener B complete. {len(stock_data)} stocks saved to {output_path}")

if __name__ == "__main__":
    main()
