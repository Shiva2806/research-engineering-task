# NLP-to-DSL Trading Strategy Engine

## Overview
This project is a research-engineering pipeline designed to convert natural language trading ideas into executable Python strategies. It bridges the gap between unstructured human instructions and structured algorithmic execution.

The pipeline performs four key steps:
1.  **NLP Parsing:** Converts English instructions (e.g., "Buy when price > SMA 20") into a structured Domain-Specific Language (DSL).
2.  **DSL Parsing:** Uses a custom Lark grammar to parse the DSL into an Abstract Syntax Tree (AST).
3.  **Code Generation:** Compiles the AST into optimized Pandas logic, including automatic validation of data columns.
4.  **Backtesting:** Simulates the strategy on historical data to calculate Total Return, Win Rate, and Drawdown.

## Project Structure
```text
Research_Engineering_Task/
├── data/
│   └── sample_data.csv        # OHLCV dataset for backtesting
├── docs/
│   └── dsl_design.md          # Grammar specification and design notes
├── src/
│   ├── nlp_engine.py          # Heuristic/Regex-based NLP parser
│   ├── dsl_parser.py          # Formal Lark grammar definition & parser
│   ├── code_generator.py      # AST -> Pandas Code converter (with validation)
│   └── backtester.py          # Event-driven trading simulator
├── main.py                    # End-to-end demonstration script
├── generate_data.py           # Helper script to create synthetic market data
└── requirements.txt           # Python dependencies
Setup & Installation
Clone or Download the Repository Navigate to the project folder in your terminal.

Install Dependencies Ensure you have Python installed, then run:

Bash

pip install -r requirements.txt
(Dependencies include pandas and lark)

Generate Data (Optional) If data/sample_data.csv is missing or you want fresh test data, run:

Bash

python generate_data.py
This creates a synthetic dataset with 200 days of OHLCV data.

Usage
Run the end-to-end demonstration script:

Bash

python main.py
What happens next?

The script simulates a user inputting a strategy:

"Buy when price is above the 20-day moving average and volume is above 1 million. Exit when RSI is below 30."

It converts this text into the DSL format:

Plaintext

ENTRY: close > SMA(close, 20) AND volume > 1000000
EXIT: RSI(close, 14) < 30
It parses this DSL into a JSON Abstract Syntax Tree (AST).

It executes the logic against sample_data.csv.

It prints a Backtest Report showing the Total Return, Number of Trades, and a Trade Log.

Architecture & Design
1. NLP Engine (src/nlp_engine.py)
Uses regex heuristics to identify trading keywords (buy, sell, crosses, above/below) and map them to DSL operators. It is designed to be robust against common stopwords like "the" or "when".

2. DSL Parser (src/dsl_parser.py)
Built using the Lark parsing library. It defines a strict grammar for the strategy language, supporting:

Comparison: >, <, >=, <=, ==, CROSSES_ABOVE

Logic: AND, OR, Nested ( )

Indicators: SMA, RSI

3. Code Generator (src/code_generator.py)
Recursively traverses the AST to build Pandas Boolean Series. It includes a Validation Layer that pre-checks if the variables (e.g., close, volume) exist in the dataset before execution, providing clear error messages instead of cryptic crashes.

4. Backtester (src/backtester.py)
A simple event-driven simulator that iterates through signals to execute trades, tracking portfolio equity and calculating max drawdown.

License
This project was created for a Research Engineering Take-Home Assignment.