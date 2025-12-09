import pandas as pd

def generate_code(ast, df):
    """
    Takes the AST (JSON) and a Pandas DataFrame.
    Returns two boolean Series: entry_signals, exit_signals
    """
    
    # --- NEW: Validation Step ---
    # We collect all variable names required by the AST
    required_columns = set()
    
    def collect_vars(node):
        if not isinstance(node, dict): return
        if node['type'] == 'variable':
            required_columns.add(node['name'])
        if 'left' in node: collect_vars(node['left'])
        if 'right' in node: collect_vars(node['right'])
        if 'args' in node:
            for arg in node['args']: collect_vars(arg)

    collect_vars(ast['entry'])
    collect_vars(ast['exit'])

    # Check if they exist in the DF (case-insensitive)
    df_cols = set(df.columns.str.lower())
    for col in required_columns:
        if col.lower() not in df_cols:
            print(f"[Error] Strategy requires column '{col}', but it is missing in the data.")
            return None, None
    # ----------------------------

    # 1. Helper to recursively evaluate nodes
    def eval_node(node):
        if not isinstance(node, dict):
            return node

        if node['type'] == 'logical':
            left = eval_node(node['left'])
            right = eval_node(node['right'])
            if node['op'] == 'AND':
                return left & right
            elif node['op'] == 'OR':
                return left | right
        
        elif node['type'] == 'comparison':
            left = eval_node(node['left'])
            right = eval_node(node['right'])
            op = node['op']
            
            if op == '>': return left > right
            elif op == '<': return left < right
            elif op == '>=': return left >= right
            elif op == '<=': return left <= right
            elif op == '==': return left == right
            elif op == 'CROSSES_ABOVE':
                return (left > right) & (left.shift(1) < right.shift(1))
            elif op == 'CROSSES_BELOW':
                return (left < right) & (left.shift(1) > right.shift(1))

        elif node['type'] == 'variable':
            return df[node['name']]
        
        elif node['type'] == 'number':
            return node['value']

        elif node['type'] == 'indicator':
            name = node['name'].upper()
            args = [eval_node(arg) for arg in node['args']]
            
            if name == 'SMA':
                series = args[0]
                window_val = args[1]
                window = int(window_val) if not isinstance(window_val, pd.Series) else 20
                return series.rolling(window).mean()
            
            elif name == 'RSI':
                series = args[0]
                window = int(args[1])
                delta = series.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
                rs = gain / loss
                return 100 - (100 / (1 + rs))

        return pd.Series(False, index=df.index)

    # 2. Evaluate Entry and Exit
    try:
        entry_signal = eval_node(ast['entry'])
        exit_signal = eval_node(ast['exit'])
        return entry_signal.fillna(False), exit_signal.fillna(False)
    except Exception as e:
        print(f"Code Generation Error: {e}")
        return None, None