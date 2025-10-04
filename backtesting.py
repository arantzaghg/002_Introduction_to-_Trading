import pandas as pd
from models import Operation
from utils import get_portfolio_value
from performance_metrics import calmar_ratio
from get_signals import get_signal
import numpy as np

def backtestings(data, SL, TP, n_shares, cash) -> pd.Series:
    data = data.copy()

    COM = 0.125 / 100 
    SL = SL
    TP = TP
    n_shares = n_shares

    active_long_positions: list[Operation] = []
    active_short_positions: list[Operation] = []
    portfolio_hist = [cash]
    trades = []

    for i, row in data.iterrows():  

        for position in active_long_positions.copy():
            if row.Close > position.take_profit or row.Close < position.stop_loss:
                profit_loss = (row.Close - position.price) * position.n_shares * (1 - COM)
                trades.append(profit_loss)
                cash += row.Close * position.n_shares * (1 - COM)
                active_long_positions.remove(position)

        for position in active_short_positions.copy():
            if row.Close < position.take_profit or row.Close > position.stop_loss:
                profit_loss = (position.price - row.Close) * position.n_shares * (1 - COM)
                trades.append(profit_loss)
                cash += (position.n_shares * position.price) + profit_loss
                active_short_positions.remove(position)

        if row.buy_signal:
            cost = row.Close * n_shares * (1 + COM)
            if cash > cost:
                cash -= cost
                active_long_positions.append(
                    Operation(
                        time=row.Datetime,
                        price=row.Close,
                        stop_loss=row.Close * (1 - SL),
                        take_profit=row.Close * (1 + TP),
                        n_shares=n_shares,
                        type='LONG'
                    )
                )

        if row.sell_signal:
            cost = row.Close * n_shares * (1 + COM)
            if cash > cost:
                cash -= cost
                active_short_positions.append(
                    Operation(
                        time=row.Datetime,
                        price=row.Close,
                        stop_loss=row.Close * (1 + SL),
                        take_profit=row.Close * (1 - TP),
                        n_shares=n_shares,
                        type='SHORT'
                    )
                )
                
       
        portfolio_hist.append(get_portfolio_value(cash, active_long_positions, active_short_positions, row.Close, n_shares))

    for position in active_long_positions.copy():
        cash += row.Close * position.n_shares * (1 - COM)

    for position in active_short_positions.copy():
        profit_loss = (position.price - row.Close) * position.n_shares * (1 - COM)
        cash += (position.n_shares * position.price) + profit_loss

    if trades:
        win = sum(1 for trade in trades if trade > 0)
        win_rate = win / len(trades)
    else:
        win_rate = 0

    active_long_positions = []
    active_short_positions = [] 

    return pd.Series(portfolio_hist), win_rate, cash


def optimize(trial, train_data) -> float:
    data = train_data.copy()

    params = {
        'rsi_window': trial.suggest_int('rsi_window', 5, 60),
        'rsi_lower':  trial.suggest_int('rsi_lower', 5, 20),
        'rsi_upper': trial.suggest_int('rsi_upper', 60, 80),
        'short_window': trial.suggest_int('short_window', 5, 40),
        'long_window': trial.suggest_int('long_window', 30, 90),
        'k_window': trial.suggest_int('k_window', 5, 20),
        'd_window': trial.suggest_int('d_window', 3, 15),
        'stop_loss': trial.suggest_float('stop_loss', 0.01, 0.05),
        'take_profit': trial.suggest_float('take_profit', 0.01, 0.05),
        'n_shares': trial.suggest_float('n_shares', 0.01, 5)
    }

    n_splits = 5
    len_data = len(data)
    calmar_ratios = []

    data = get_signal(data, params)

    for i in range(n_splits):
        size = len_data // n_splits
        start = i * size
        end = (i + 1) * size
        split_data = data.iloc[start:end,:]
        portfolio_values, win_rate, cash = backtestings(split_data, params['stop_loss'], params['take_profit'], params['n_shares'], cash=1_000_000)

        calmar = calmar_ratio(portfolio_values)
        calmar_ratios.append(calmar)

    return np.mean(calmar_ratios)
    