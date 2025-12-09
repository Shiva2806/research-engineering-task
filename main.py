import pandas as pd
import json
from src.nlp_engine import parse_natural_language
from src.dsl_parser import parse_dsl
from src.code_generator import generate_code
from src.backtester import Backtester

def main():
    print("=== AI Trading Strategy Generator ===\n")

    # 1. Load Data
    try:
        # Check if the file exists and load it
        df = pd.read_csv('data/sample_data.csv')
        # Standardize column names (remove spaces, lowercase)
        df.columns = df.columns.str.strip().str.lower()
        
        # Ensure 'date' is datetime objects
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            
        print(f"[OK] Loaded data: {len(df)} rows")
    except Exception as e:
        print(f"[Error] Could not load data: {e}")
        print("Make sure 'data/sample_data.csv' exists and has content.")
        return

    # 2. Get User Input (Example from PDF)
    user_input = "Buy when price is above the 20-day moving average and volume is above 1 million. Exit when RSI is below 30."
    print(f"\nNatural Language Input:\n'{user_input}'")

    # 3. NLP -> DSL
    dsl_text = parse_natural_language(user_input)
    print(f"\n[1] Generated DSL:\n{dsl_text}")

    # 4. DSL -> AST
    ast = parse_dsl(dsl_text)
    if "error" in ast:
        print(f"\n[Error] Parsing Failed: {ast['error']}")
        return
    # Print AST nicely
    print(f"\n[2] Parsed AST (JSON):\n{json.dumps(ast, indent=2)}")

    # 5. AST -> Python Code (Execution)
    # We pass the dataframe so the generator can evaluate indicators
    entry_signals, exit_signals = generate_code(ast, df)
    
    if entry_signals is None:
        print("\n[Error] Code Generation Failed")
        return
    
    # Calculate how many buy signals we found
    buy_count = entry_signals.sum()
    print(f"\n[3] Strategy Executed. Found {buy_count} entry signals.")

    # 6. Backtest
    tester = Backtester()
    results = tester.run(df, entry_signals, exit_signals)

    print("\n[4] Backtest Results:")
    print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    main()