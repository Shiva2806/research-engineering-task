
# NLP-to-DSL Trading Strategy Engine

## Overview
This project is a research-engineering pipeline designed to convert natural language trading ideas into executable Python strategies.  
It bridges the gap between unstructured human instructions and structured algorithmic execution.

The pipeline performs four key steps:

1. **NLP Parsing:** Converts English trading instructions (e.g., *"Buy when price > SMA 20"*) into a structured Domain-Specific Language (DSL).  
2. **DSL Parsing:** Uses a custom Lark grammar to convert DSL into an Abstract Syntax Tree (AST).  
3. **Code Generation:** Compiles the AST into optimized Pandas logic, with automatic validation of data columns.  
4. **Backtesting:** Simulates the strategy on historical data and computes performance metrics like Total Return, Win Rate, and Drawdown.

---

## Project Structure
```text
Research_Engineering_Task/
├── data/
│   └── sample_data.csv        # OHLCV dataset for backtesting
├── docs/
│   └── dsl_design.md          # Grammar specification and design notes
├── src/
│   ├── nlp_engine.py          # Heuristic/Regex-based NLP parser
│   ├── dsl_parser.py          # Lark grammar definition & DSL parser
│   ├── code_generator.py      # AST → Pandas code generator (with validation)
│   └── backtester.py          # Event-driven trading simulator
├── main.py                    # End-to-end demonstration script
├── generate_data.py           # Script to generate synthetic OHLCV data
└── requirements.txt           # Python dependencies
````

---

## Setup & Installation

### 1. Clone or Download the Repository

Navigate to the project folder in your terminal.

### 2. Install Dependencies

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

Dependencies include:

* pandas
* lark

---

## Generate Data (Optional)

If `data/sample_data.csv` is missing or you want fresh test data, run:

```bash
python generate_data.py
```

This creates a synthetic dataset with **200 days of OHLCV data**.

---

## Usage

Run the full pipeline using:

```bash
python main.py
```

---

## What Happens Next?

The script simulates a user inputting the following strategy:

> **"Buy when price is above the 20-day moving average and volume is above 1 million.
> Exit when RSI is below 30."**

### Generated DSL:

```
ENTRY: close > SMA(close, 20) AND volume > 1000000
EXIT: RSI(close, 14) < 30
```

### Pipeline Flow:

1. Converts NLP → DSL
2. Parses DSL → AST
3. Generates executable Pandas logic
4. Runs a backtest on `sample_data.csv`
5. Prints:

* Total Return
* Number of Trades
* Trade Log

---

## Architecture & Design

### 1. NLP Engine (`src/nlp_engine.py`)

* Uses regex and heuristics
* Detects trading concepts: buy, sell, crosses, above/below, indicators
* Handles stopwords naturally

### 2. DSL Parser (`src/dsl_parser.py`)

Built using **Lark**, includes grammar support for:

* **Comparison Operators:**
  `>`, `<`, `>=`, `<=`, `==`, `CROSSES_ABOVE`
* **Logical Operators:**
  `AND`, `OR`, nested parentheses
* **Indicators:**
  `SMA`, `RSI`

### 3. Code Generator (`src/code_generator.py`)

* Converts AST nodes into Pandas Boolean Series
* Includes validation layer:

  * Ensures all required columns exist
  * Produces human-readable errors

### 4. Backtester (`src/backtester.py`)

* Simple event-driven system
* Simulates entry/exit signals
* Tracks portfolio value, equity curve, returns, drawdown

---
