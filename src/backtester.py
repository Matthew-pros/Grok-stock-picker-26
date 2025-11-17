import yfinance as yf
import pandas as pd

def backtest_portfolio(picks, start_date, end_date):
    returns = []
    for pick in picks:
        ticker = pick['ticker']
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        if not hist.empty:
            ret = (hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]
            returns.append(ret)
    avg_return = np.mean(returns) if returns else 0
    return {'avg_return': avg_return, 'picks': len(picks)}
