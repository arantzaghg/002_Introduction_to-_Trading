import pandas as pd
from utils import split_fun
import optuna
from backtesting import backtest, backtest_with_params
import matplotlib.pyplot as plt


def main():
    data = pd.read_csv('Binance_BTCUSDT_1h.csv', skiprows=1).dropna()
    data = data.rename(columns={'Date': 'Datetime'})
    data['Datetime'] = pd.to_datetime(data['Datetime'], format = 'mixed', dayfirst=True)
    data = data.iloc[::-1].reset_index(drop=True)

    train, test, validation = split_fun(data)

    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: backtest(train, trial), n_trials=10)
    cash, portfolio_value = backtest_with_params(train, study.best_trial.params)
    print(cash)
    plt.plot(portfolio_value)
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.show()


    
   
if __name__ == "__main__":
    main()
