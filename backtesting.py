import pandas as pd
from models import Operation
from indicators import rsi, ema, stochastic_oscillator
from utils import get_portfolio_value
from utils import get_portfolio_value
from performance_metrics import calmar_ratio


def backtest(data, trail) -> float:
    data = data.copy()

    rsi_window = trail.suggest_int('rsi_window', 5, 50)
    rsi_lower = trail.suggest_int('rsi_lower', 5, 35)
    rsi_upper = trail.suggest_int('rsi_upper', 65, 95)

    short_window = trail.suggest_int('short_window', 5, 20)
    long_window = trail.suggest_int('long_window', 30, 100)

    k_window = trail.suggest_int('k_window', 5, 20)
    d_window = trail.suggest_int('d_window', 3, 10)

    stop_loss = trail.suggest_float('stop_loss', 0.01, 0.15)
    take_profit = trail.suggest_float('take_profit', 0.01, 0.15)
    n_shares = trail.suggest_int('n_shares', 50, 500)

    rsi_buy, rsi_sell = rsi(data, rsi_window, rsi_lower, rsi_upper)
    ema_buy, ema_sell = ema(data, short_window, long_window)
    stoch_buy, stoch_sell = stochastic_oscillator(data, k_window, d_window)

    historic = data.dropna()
    historic['buy_signal'] = (rsi_buy.astype(int) + ema_buy.astype(int) + stoch_buy.astype(int)) >= 2
    historic['sell_signal'] = (rsi_sell.astype(int) + ema_sell.astype(int) + stoch_sell.astype(int)) >= 2  

    COM = 0.125 / 100
    SL = stop_loss
    TP = take_profit
    cash = 1_000_000

    active_long_positions: list[Operation] = []
    active_short_positions: list[Operation] = []
    portfolio_values = []

    for i, row in historic.iterrows():  

        for position in active_long_positions.copy():
            if row.Close >= position.take_profit or row.Close <= position.stop_loss:
                val += row.Close * position.n_shares * (1 - COM)
                active_long_positions.remove(position)

        for position in active_short_positions.copy():
            if row.Close <= position.take_profit or row.Close >= position.stop_loss:
                profit_loss = (position.price - row.Close) * position.n_shares *(1-COM)
                val += (position.n_shares * position.n_shares * (1 + COM)) + profit_loss
                active_short_positions.remove(position)

        if row.buy_signal:
            if cash >= row.Close * n_shares * (1 + COM):
                cash -= row.Close * n_shares * (1 + COM)
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
            if cash >= row.Close * n_shares * (1 + COM):
                cash -= row.Close * n_shares * (1 + COM)
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

        portfolio_values.append(get_portfolio_value(cash, active_long_positions, active_short_positions, row.Close, n_shares, COM))
    

    for position in active_long_positions:
        profit_loss = (row.Close - position.price) * position.n_shares * (1 - COM)
        cash += position.n_shares * row.Close * (1 - COM)

    for position in active_short_positions:
        profit_loss = (position.price - row.Close) * position.n_shares * (1 - COM)
        cash += (position.n_shares * position.price * (1 - COM)) + profit_loss

    active_long_positions = []
    active_short_positions = []

    calmar_df = pd.DataFrame(portfolio_values, columns=['Portfolio Value'])
    calmar_val = calmar_ratio(calmar_df['Portfolio Value']) 

    return calmar_val



def backtest_with_params(data: pd.DataFrame, params) -> float:
    data = data.copy()

    rsi_window = params['rsi_window']
    rsi_lower = params['rsi_lower']
    rsi_upper = params['rsi_upper']
    rsi_buy, rsi_sell = rsi(data, rsi_window, rsi_lower, rsi_upper)

    short_window = params['short_window']
    long_window = params['long_window']
    ema_buy, ema_sell = ema(data, short_window, long_window)

    k_window = params['k_window']
    d_window = params['d_window']
    stoch_buy, stoch_sell = stochastic_oscillator(data, k_window, d_window)

    SL = params['stop_loss']
    TP = params['take_profit']
    n_shares = params['n_shares']

    historic = data.dropna()
    historic['buy_signal'] = (rsi_buy.astype(int) + ema_buy.astype(int) + stoch_buy.astype(int)) >= 2
    historic['sell_signal'] = (rsi_sell.astype(int) + ema_sell.astype(int) + stoch_sell.astype(int)) >= 2  

    COM = 0.125 / 100 
    cash = 1_000_000

    active_long_positions: list[Operation] = []
    active_short_positions: list[Operation] = []
    portfolio_values = []

    for i, row in historic.iterrows():  
        for position in active_long_positions.copy():
            if row.Close >= position.take_profit or row.Close <= position.stop_loss:
                profit_loss = (row.Close - position.price) * position.n_shares * (1 - COM)
                cash += row.Close * position.n_shares * (1 - COM)
                active_long_positions.remove(position)

        for position in active_short_positions.copy():
            if row.Close <= position.take_profit or row.Close >= position.stop_loss:
                profit_loss = (position.price - row.Close) * position.n_shares * (1 - COM)
                cash += (position.n_shares * position.price * (1 - COM)) + profit_loss
                active_short_positions.remove(position)

        if row.buy_signal:
            if cash >= row.Close * n_shares * (1 + COM):
                cash -= row.Close * n_shares * (1 + COM)
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
            if cash >= row.Close * n_shares * (1 + COM):
                cash -= row.Close * n_shares * (1 + COM)
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

        portfolio_values.append(get_portfolio_value(cash, active_long_positions, active_short_positions, row.Close, n_shares, COM))
    
    for position in active_long_positions:
        cash += position.n_shares * row.Close * (1 - COM)

    for position in active_short_positions:
        profit_loss = (position.price - row.Close) * position.n_shares * (1 - COM)
        cash += (position.n_shares * position.price * (1 - COM)) + profit_loss

    active_long_positions = []
    active_short_positions = [] 

    return cash, portfolio_values

