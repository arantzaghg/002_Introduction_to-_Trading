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


    train, test, validation = split_fun(data)
    
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: optimize(trial, train), n_trials=20, n_jobs=-1)

    train = get_signal(train.copy(), study.best_params)
    portfolio_val_train = backtestings(train, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'])
    portfolio_val_test = backtestings(train, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'])

    portfolio_val_validation = backtestings(train, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'])

    test_validation = pd.concat([test, validation]).reset_index(drop=True)
    total_portfolio = portfolio_val_test + portfolio_val_validation

    


    test_df = pd.DataFrame({
        'Date': test['Datetime'].reset_index(drop=True),
        'Portfolio Value': portfolio_val_test
    })

    validation_df = pd.DataFrame({
        'Date': validation['Datetime'].reset_index(drop=True),
        'Portfolio Value': portfolio_val_validation
    })
    
    plt.figure(figsize=(12, 6))
    plt.plot(test_df['Date'], test_df['Portfolio Value'], label='Test', color='red')
    plt.plot(validation_df['Date'], validation_df['Portfolio Value'], label='Validation', color='green')
    plt.title('Portfolio value over time (test + validation)')
    plt.xlabel('Date')
    plt.ylabel('Portfolio value')
    plt.legend()
    plt.show()





# 3 comillas codigos
    
   
if __name__ == "__main__":
    main()
