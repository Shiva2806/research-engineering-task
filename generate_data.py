import pandas as pd
import numpy as np
import os

# Create 200 days of dummy data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=200)
close_prices = 100 + np.cumsum(np.random.randn(200))  # Random walk price

data = {
    'date': dates,
    'open': close_prices,
    'high': close_prices + 2,
    'low': close_prices - 2,
    'close': close_prices,
    # Random volume between 800k and 1.2M
    'volume': np.random.randint(800000, 1200000, 200) 
}

df = pd.DataFrame(data)

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Save to the existing data file path
df.to_csv('data/sample_data.csv', index=False)
print("✅ Success: Overwrote 'data/sample_data.csv' with 200 rows of data.")