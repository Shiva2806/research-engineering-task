from lark import Lark, Transformer, v_args
import json

# 1. Define the Grammar
# FIXED: Added '?' to start and condition_block to prevent "Tree" wrappers
dsl_grammar = """
    ?start: strategy

    strategy: "ENTRY:" condition_block "EXIT:" condition_block -> make_strategy

    ?condition_block: logical_expr

    ?logical_expr: logical_expr "AND" comparison  -> logical_and
                 | logical_expr "OR" comparison   -> logical_or
                 | comparison

    ?comparison: term COMPARATOR term           -> compare_op
               | "(" logical_expr ")"

    ?term: indicator
         | variable
         | number

    indicator: NAME "(" arg_list ")"
    
    arg_list: term ("," term)*

    variable: NAME
    number: NUMBER

    COMPARATOR: ">=" | "<=" | "==" | ">" | "<" | "CROSSES_ABOVE" | "CROSSES_BELOW"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

# 2. Build the AST (The Transformer)
class TradingDSLTransformer(Transformer):
    def make_strategy(self, args):
        return {
            "entry": args[0],
            "exit": args[1]
        }

    def logical_and(self, args):
        return {"type": "logical", "op": "AND", "left": args[0], "right": args[1]}

    def logical_or(self, args):
        return {"type": "logical", "op": "OR", "left": args[0], "right": args[1]}

    def compare_op(self, args):
        return {
            "type": "comparison",
            "left": args[0],
            "op": args[1].value, 
            "right": args[2]
        }

    def indicator(self, args):
        name = args[0].value
        params = args[1] 
        return {"type": "indicator", "name": name, "args": params}

    def arg_list(self, args):
        return args

    def variable(self, args):
        return {"type": "variable", "name": args[0].value}

    def number(self, args):
        return {"type": "number", "value": float(args[0].value)}

# 3. Public Parse Function
parser = Lark(dsl_grammar, parser='lalr', transformer=TradingDSLTransformer())

def parse_dsl(text):
    try:
        # parser.parse returns the dict directly now because of the '?' rules
        return parser.parse(text)
    except Exception as e:
        return {"error": str(e)}

# --- Quick Test Block ---
if __name__ == "__main__":
    test_dsl = """
    ENTRY: close > SMA(close, 20) AND volume > 1000000
    EXIT: RSI(close, 14) < 30
    """
    ast = parse_dsl(test_dsl)
    print(json.dumps(ast, indent=2))