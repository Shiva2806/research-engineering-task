# Domain-Specific Language (DSL) Design Specification

## 1. Overview
The DSL is designed to be human-readable yet strictly structured for parsing. It separates a trading strategy into two distinct logic blocks: **ENTRY** signals (buying) and **EXIT** signals (selling).

## 2. Grammar Specification
The language follows a strict `KEYWORD: CONDITION` format.

### Structure
```text
ENTRY: <Boolean Expression>
EXIT:  <Boolean Expression>
````

### Supported Operators

  * **Comparison:** `>`, `<`, `>=`, `<=`, `==`
  * **Crossover Events:** `CROSSES_ABOVE`, `CROSSES_BELOW`
      * *Logic:* `A CROSSES_ABOVE B` implies `(Current A > Current B) AND (Previous A < Previous B)`
  * **Boolean Logic:** `AND`, `OR`
  * **Grouping:** `( ... )` for nested conditions.

### Indicators & Variables

  * **Variables:** `close`, `open`, `high`, `low`, `volume`
  * **Indicators:**
      * `SMA(source, period)` e.g., `SMA(close, 20)`
      * `RSI(source, period)` e.g., `RSI(close, 14)`
  * **Literals:** Numbers (integers or floats).

## 3\. Examples

**Example 1: Simple Moving Average Strategy**

```text
ENTRY: close > SMA(close, 20) AND volume > 1000000
EXIT: close < SMA(close, 20)
```

**Example 2: Mean Reversion (RSI) with Stop Loss Logic**

```text
ENTRY: RSI(close, 14) < 30
EXIT: RSI(close, 14) > 70 OR close < 95
```

## 4\. Design Assumptions

1.  **Data Availability:** The system assumes the input DataFrame contains standard OHLCV columns (`open`, `high`, `low`, `close`, `volume`).
2.  **Case Insensitivity:** The NLP engine normalizes input to lowercase, but the DSL parser expects keywords (AND, OR, ENTRY) to be standardized (handled by the pipeline).
3.  **Validation:** The execution engine validates that all referenced variables exist in the dataset before execution to prevent runtime crashes.

<!-- end list -->
