import re

def parse_natural_language(text):
    """
    Converts English text into DSL format.
    Example: "Buy when close > 50" -> "ENTRY: close > 50 EXIT: ..."
    """
    text = text.lower()
    
    # 1. Split into Entry and Exit logic
    entry_part = "close > SMA(close, 20)" 
    exit_part = "close < SMA(close, 20)"

    if "exit" in text or "sell" in text:
        parts = re.split(r'\b(exit|sell)\b', text)
        if len(parts) > 1:
            raw_entry = parts[0]
            raw_exit = parts[2]
            entry_part = convert_rules(raw_entry)
            exit_part = convert_rules(raw_exit)
    else:
        entry_part = convert_rules(text)

    return f"ENTRY: {entry_part}\nEXIT: {exit_part}"

def convert_rules(text):
    """
    Applies regex substitutions to convert English phrases to DSL.
    """
    # 1. Clean up common stopwords/punctuation
    text = text.replace(".", "")  # Remove periods
    text = text.replace(",", "")  # Remove commas
    text = text.replace(" the ", " ") # Remove 'the'
    text = text.replace(" when ", " ") # Remove 'when' inside sentences
    
    # 2. Normalize Logic (and, or)
    text = text.replace(" and ", " AND ").replace(" or ", " OR ")

    # 3. Normalize Variables
    text = text.replace("price", "close")
    
    # 4. Handle Indicators
    text = re.sub(r'(\d+)[- ]?day moving average', r'SMA(close, \1)', text)
    text = re.sub(r'sma (\d+)', r'SMA(close, \1)', text)
    text = re.sub(r'rsi', r'RSI(close, 14)', text)

    # 5. Handle Comparators
    text = text.replace(" is above ", " > ")
    text = text.replace(" is below ", " < ")
    text = text.replace(" above ", " > ")
    text = text.replace(" below ", " < ")
    text = text.replace(" crosses above ", " CROSSES_ABOVE ")
    text = text.replace(" crosses below ", " CROSSES_BELOW ")
    text = text.replace(" = ", " == ")

    # 6. Handle "Buy" / "Enter" / "Trigger" cleanup at start
    # This regex removes "buy when", "enter if", "trigger entry" etc.
    text = re.sub(r'^(buy|enter|trigger entry|exit|sell)\s*(when|if)?\s*', '', text.strip())

    # 7. Numbers (1 million -> 1000000)
    text = text.replace("1 million", "1000000")
    text = text.replace("1m", "1000000")

    return text.strip()

# --- Quick Test Block ---
if __name__ == "__main__":
    input_text = "Buy when price is above the 20-day moving average and volume is above 1 million. Exit when RSI is below 30."
    dsl = parse_natural_language(input_text)
    print("Generated DSL:\n", dsl)