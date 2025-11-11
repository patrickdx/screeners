# Adding New Screeners - Quick Start Guide

## 🎯 Overview

Your screener system is now set up with a **standardized interface** that makes adding new screeners easy and consistent.

## 📋 What's Been Created

### 1. **Momentum Screener** (`scripts/screener_momentum.py`)
- Converted from your original `momentum.py`
- Finds stocks breaking out to 52-week highs with strong relative strength
- Fully automated (no user input required)
- Outputs to `data/screener_momentum.json`

### 2. **Screener Template** (`scripts/screener_template.py`)
- Complete blueprint for creating new screeners
- Includes detailed comments and documentation
- Built-in integration checklist
- Follow this pattern for all new screeners

## 🚀 How to Add a New Screener (5 Steps)

### Step 1: Create the Python Script
```bash
# Copy the template
cp scripts/screener_template.py scripts/screener_YOUR_NAME.py
```

Edit your new file and implement:
1. **CONFIG** - Set your parameters
2. **calculate_screener()** - Your screening logic
3. **Output format** - List of dicts with consistent keys

### Step 2: Update the Workflow
Edit `.github/workflows/run_screeners.yml`:
```yaml
- name: Run Python Screeners
  run: |
    python scripts/screener_A.py
    python scripts/screener_B.py
    python scripts/screener_momentum.py
    python scripts/screener_YOUR_NAME.py  # <-- Add this line
```

### Step 3: Update JavaScript Config
Edit `app.js` - add to `tableConfig`:
```javascript
screenerYourName: {
    file: "data/screener_YOUR_NAME.json",
    columns: [
        { "title": "Ticker", "data": "ticker" },
        { "title": "Your Metric", "data": "your_metric" },
        // ... your columns
    ]
}
```

### Step 4: Add Button to HTML
Edit `index.html`:
```html
<button id="loadScreenerYourName">📊 Your Screener Name</button>
```

### Step 5: Add Click Handler
Edit `app.js` - add in the `$(document).ready()` section:
```javascript
$('#loadScreenerYourName').on('click', function() {
    loadScreenerData(tableConfig.screenerYourName);
});
```

## 🔍 The Screener Interface Contract

Every screener MUST follow this interface:

### ✅ Required Output Format
```python
{
    "data": [
        {
            "ticker": "AAPL",
            "metric1": 123.45,
            "metric2": "value",
            # ... your fields
        },
        # ... more stocks
    ]
}
```

### ✅ Required Structure
```python
import json
import os

def calculate_screener():
    """Your screening logic here"""
    results = []  # List of dicts
    return results

def main():
    try:
        results = calculate_screener()
        os.makedirs("data", exist_ok=True)
        with open("data/screener_NAME.json", 'w') as f:
            json.dump({"data": results}, f, indent=2)
        print(f"✓ Screener complete. {len(results)} stocks saved")
    except Exception as e:
        print(f"❌ Error: {e}")
        # Save empty data on error
        os.makedirs("data", exist_ok=True)
        with open("data/screener_NAME.json", 'w') as f:
            json.dump({"data": []}, f)

if __name__ == "__main__":
    main()
```

## 📊 Current Screeners

| Screener | File | Description |
|----------|------|-------------|
| Daily Gainers | `screener_A.py` | Stocks with high daily gains |
| Oversold Signals | `screener_B.py` | RSI-based oversold stocks |
| Momentum Breakouts | `screener_momentum.py` | 52-week high breakouts with volume |

## 🧪 Testing Your Screener

### Local Testing
```bash
# 1. Run your screener
python scripts/screener_YOUR_NAME.py

# 2. Check the output
cat data/screener_YOUR_NAME.json

# 3. Start web server
python -m http.server 8000

# 4. Open browser
# Navigate to: http://localhost:8000
# Click your button to test
```

### Verify Output Format
Your JSON should look like:
```json
{
  "data": [
    {"ticker": "AAPL", "field1": 123, "field2": "value"},
    {"ticker": "MSFT", "field1": 456, "field2": "value"}
  ]
}
```

## 🎨 Frontend Column Mapping

The column configuration maps JSON keys to table headers:

```javascript
columns: [
    { 
        "title": "What Shows in Table Header",  // User sees this
        "data": "json_key_name"                  // Maps to this JSON field
    }
]
```

## 💡 Best Practices

1. **Error Handling**: Always catch exceptions and output empty data on failure
2. **Logging**: Print clear status messages
3. **Configuration**: Use CONSTANTS at the top for easy tweaking
4. **No User Input**: Scripts must run fully automated
5. **Consistent Keys**: Use snake_case for JSON keys
6. **Round Numbers**: Round floats to 2 decimal places for display

## 🔄 Development Workflow

```bash
# 1. Create new screener from template
cp scripts/screener_template.py scripts/screener_myname.py

# 2. Edit and implement logic
code scripts/screener_myname.py

# 3. Test locally
python scripts/screener_myname.py

# 4. Verify output
cat data/screener_myname.json

# 5. Add to workflow
code .github/workflows/run_screeners.yml

# 6. Update frontend
code app.js index.html

# 7. Test in browser
python -m http.server 8000

# 8. Commit and push
git add .
git commit -m "Add new screener: myname"
git push
```

## 📦 Dependencies

Add new packages to `requirements.txt`:
```txt
yfinance>=0.2.32      # Already included
pandas>=2.1.3         # Already included
your-new-package      # Add if needed
```

## 🎯 Key Files Reference

| File | Purpose |
|------|---------|
| `scripts/screener_template.py` | Blueprint for new screeners |
| `scripts/screener_*.py` | Individual screener implementations |
| `.github/workflows/run_screeners.yml` | Automated daily runs |
| `app.js` | Frontend table configurations |
| `index.html` | UI buttons |
| `data/screener_*.json` | Output data files |
| `requirements.txt` | Python dependencies |

## ✅ Integration Checklist

Use this checklist when adding a new screener:

- [ ] Copy template to `scripts/screener_NAME.py`
- [ ] Implement screening logic
- [ ] Test locally: `python scripts/screener_NAME.py`
- [ ] Verify JSON output exists and is valid
- [ ] Add to workflow YAML
- [ ] Add table config to `app.js`
- [ ] Add button to `index.html`
- [ ] Add click handler to `app.js`
- [ ] Update `requirements.txt` if needed
- [ ] Test in browser with local server
- [ ] Update README with screener description
- [ ] Commit and push

## 🚀 Your System is Ready!

You now have a **production-ready, scalable screener platform**. Just follow the template and checklist to add unlimited screeners!
