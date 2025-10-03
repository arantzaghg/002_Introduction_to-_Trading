import pandas as pd
from utils import split_fun
import optuna
from backtesting import backtestings, optimize
import matplotlib.pyplot as plt
from get_signals import get_signal
from performance_metrics import all_metrics


def main():
    data = pd.read_csv('Binance_BTCUSDT_1h.csv', skiprows=1).dropna()
    data = data.rename(columns={'Date': 'Datetime'})
    data['Datetime'] = pd.to_datetime(data['Datetime'], format = 'mixed', dayfirst=True)
    data = data.iloc[::-1].reset_index(drop=True)
    print(data.head())

    train, test, validation = split_fun(data)
    
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: optimize(trial, train), n_trials=10, n_jobs=-1)

    train = get_signal(train.copy(), study.best_params)
    portfolio_val = backtestings(train, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'])
    print(portfolio_val)

    plt.plot(portfolio_val)
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.show()
    
    all_met = all_metrics(portfolio_val)
    print(all_met)

# 3 comillas codigos
    
   
if __name__ == "__main__":
    main()
