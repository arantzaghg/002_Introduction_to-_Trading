import ta
import pandas as pd


def get_signal(data: pd.DataFrame, params:dict) -> pd.DataFrame:
    data = data.copy()

    rsi_window = params['rsi_window']
    rsi_lower = params['rsi_lower']
    rsi_upper = params['rsi_upper']
    short_window = params['short_window']
    long_window = params['long_window']
    k_window = params['k_window']
    d_window = params['d_window']

    rsi_indicator = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
    rsi = rsi_indicator.rsi()
    buy_signal_rsi = rsi < rsi_lower
    sell_signal_rsi = rsi > rsi_upper

    short_ema = ta.trend.EMAIndicator(data.Close, window=short_window).ema_indicator()
    long_ema = ta.trend.EMAIndicator(data.Close, window=long_window).ema_indicator()
    buy_signal_ema = short_ema > long_ema
    sell_signal_ema = short_ema < long_ema

    stoch_indicator = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'], window=k_window, smooth_window=d_window)
    stoch_k = stoch_indicator.stoch()
    stoch_d = stoch_indicator.stoch_signal()
    buy_signal_stoch = (stoch_k < 20) & (stoch_d < 20) & (stoch_k > stoch_d)
    sell_signal_stoch = (stoch_k > 80) & (stoch_d > 80) & (stoch_k < stoch_d)

    data['buy_signal'] = (buy_signal_rsi.astype(int) + buy_signal_ema.astype(int) + buy_signal_stoch.astype(int)) >= 2
    data['sell_signal'] = (sell_signal_rsi.astype(int) + sell_signal_ema.astype(int) + sell_signal_stoch.astype(int)) >= 2

    return data

   
