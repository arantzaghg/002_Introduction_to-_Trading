import pandas as pd
import ta

def rsi(data: pd.DataFrame, rsi_window: int, rsi_lower: int, rsi_upper: int) -> tuple:
    rsi_indicator = ta.momentum.RSIIndicator(data['Close'], window=rsi_window)
    rsi = rsi_indicator.rsi()

    buy_signal_rsi = rsi < rsi_lower
    sell_signal_rsi = rsi > rsi_upper

    return buy_signal_rsi, sell_signal_rsi

def ema(data: pd.DataFrame, short_window: int, long_window: int) -> tuple:
    short_ema = ta.trend.EMAIndicator(data['Close'], window=short_window).ema_indicator()
    long_ema = ta.trend.EMAIndicator(data['Close'], window=long_window).ema_indicator()

    buy_signal_ema = short_ema > long_ema
    sell_signal_ema = short_ema < long_ema

    return buy_signal_ema, sell_signal_ema

def stochastic_oscillator(data: pd.DataFrame, k_window: int, d_window: int) -> tuple:
    stoch_indicator = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'], window=k_window, smooth_window=d_window)
    stoch_k = stoch_indicator.stoch()
    stoch_d = stoch_indicator.stoch_signal()

    buy_signal_stoch = (stoch_k < 20) & (stoch_d < 20) & (stoch_k > stoch_d)
    sell_signal_stoch = (stoch_k > 80) & (stoch_d > 80) & (stoch_k < stoch_d)

    return buy_signal_stoch, sell_signal_stoch
