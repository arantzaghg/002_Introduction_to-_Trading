import pandas as pd
import numpy as np

def sharpe_ratio(portfolio_hist) -> float:
    returns = portfolio_hist.pct_change().dropna()
    mean_return = returns.mean()
    std_return = returns.std()
        
    annual_return = mean_return * (365 * 24)
    annual_std = std_return * np.sqrt(365 * 24)
    
    return annual_return / annual_std if annual_std > 0 else 0

def sortino_ratio(portfolio_hist) -> float:
    returns = portfolio_hist.pct_change().dropna()
    mean_return = returns.mean()
    downside_dev = returns[returns < 0].std()

    annual_return = mean_return * (365 * 24)
    annual_downside_dev = downside_dev * np.sqrt(365 * 24)

    return annual_return / annual_downside_dev if annual_downside_dev > 0 else 0
    

def maximum_drawdown(portfolio_hist) -> float:
    rolling_max = portfolio_hist.cummax()
    drawdown = (rolling_max - portfolio_hist) / rolling_max
    max_drawdown = abs(drawdown.max())

    return max_drawdown
    

def calmar_ratio(portfolio_hist) -> float:
    returns = portfolio_hist.pct_change().dropna()
    mean_return = returns.mean()
    annual_return = mean_return * (365 * 24)  

    max_drawdown = maximum_drawdown(portfolio_hist)
    
    return annual_return / max_drawdown if max_drawdown > 0 else 0

def win_rate(trades: list) -> float:
    if not trades:
        return 0
    
    wins = sum(1 for trade in trades if trade['profit'] > 0)

    return wins / len(trades)

def all_metrics(portfolio_value) -> pd.DataFrame:
    metrics = {
        'Sharpe Ratio': sharpe_ratio(portfolio_value),
        'Sortino Ratio': sortino_ratio(portfolio_value),
        'Maximum Drawdown': maximum_drawdown(portfolio_value),
        'Calmar Ratio': calmar_ratio(portfolio_value)
    }
    
    return pd.DataFrame([metrics])
