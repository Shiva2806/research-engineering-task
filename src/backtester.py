import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.trades = []
        self.equity_curve = []

    def run(self, df, entry_signals, exit_signals):
        """
        Simulates trading based on signals.
        """
        position = 0      # 0 = flat, >0 = entry price
        entry_date = None
        
        # Ensure signals align with DataFrame
        entry_signals = entry_signals.values
        exit_signals = exit_signals.values
        prices = df['close'].values
        dates = df['date'].values if 'date' in df.columns else df.index

        for i in range(len(df)):
            price = prices[i]
            date = dates[i]

            # Logic: If no position, check Entry. If position, check Exit.
            if position == 0:
                if entry_signals[i]:
                    position = price
                    entry_date = date
            
            elif position > 0:
                if exit_signals[i]:
                    exit_price = price
                    pnl = (exit_price - position) / position
                    self.trades.append({
                        'entry_date': entry_date,
                        'exit_date': date,
                        'entry_price': position,
                        'exit_price': exit_price,
                        'pnl_pct': pnl
                    })
                    position = 0 # Reset position
        
        return self.generate_report()

    def generate_report(self):
        if not self.trades:
            return "No trades executed."

        trades_df = pd.DataFrame(self.trades)
        total_return = trades_df['pnl_pct'].sum() * 100
        avg_trade = trades_df['pnl_pct'].mean() * 100
        win_rate = len(trades_df[trades_df['pnl_pct'] > 0]) / len(trades_df) * 100
        
        # Simple Drawdown Calculation (Cumulative sum of returns)
        cum_returns = (1 + trades_df['pnl_pct']).cumprod()
        peak = cum_returns.cummax()
        drawdown = (cum_returns - peak) / peak
        max_drawdown = drawdown.min() * 100

        return {
            "Total Return (%)": round(total_return, 2),
            "Max Drawdown (%)": round(max_drawdown, 2),
            "Total Trades": len(trades_df),
            "Win Rate (%)": round(win_rate, 2),
            "Trade Log": trades_df.tail(5).to_dict('records') # Show last 5 trades
        }

# --- Quick Test Block ---
if __name__ == "__main__":
    # Create fake data
    dates = pd.date_range(start='2023-01-01', periods=10)
    data = {'date': dates, 'close': [100, 105, 102, 110, 115, 112, 120, 118, 125, 130]}
    df = pd.DataFrame(data)

    # Fake Signals: Buy on Day 1 (Index 0), Sell on Day 4 (Index 3)
    entry = pd.Series([True, False, False, False, True, False, False, False, False, False])
    exit =  pd.Series([False, False, False, True, False, False, False, True, False, False])

    tester = Backtester()
    results = tester.run(df, entry, exit)
    
    import json
    print(json.dumps(results, indent=2, default=str))