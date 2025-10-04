import pandas as pd
from utils import split_fun
import optuna
from backtesting import backtestings, optimize
from get_signals import get_signal
from performance_metrics import all_metrics
from plots import port_val, test_val
from tables import create_table



def main():
    data = pd.read_csv('Binance_BTCUSDT_1h.csv', skiprows=1).dropna()
    data = data.rename(columns={'Date': 'Datetime'})
    data['Datetime'] = pd.to_datetime(data['Datetime'], format='mixed', dayfirst=True)
    data = data.iloc[::-1].reset_index(drop=True)

    train, test, validation = split_fun(data)

    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: optimize(trial, train), n_trials=10)

    print("Best parameters:", study.best_params)
    print("Best Value:", study.best_value)

    train_data = get_signal(train.copy(), study.best_params)
    portfolio_value_train, win_rate = backtestings(train_data, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'])

    test_data = get_signal(test.copy(), study.best_params)
    portfolio_value_test, win_rate = backtestings(test_data, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'])

    validation_data = get_signal(validation.copy(), study.best_params)
    portfolio_value_validation, win_rate = backtestings(validation_data, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'])

    shift = portfolio_value_test.iloc[-1] - portfolio_value_validation.iloc[0]
    portfolio_value_validation = portfolio_value_validation + shift

    combined = pd.concat([test_data, validation_data]).reset_index(drop=True)
    test_val_portfolio = portfolio_value_test + portfolio_value_validation   

    port_val(portfolio_value_train)
    test_val(portfolio_value_test, portfolio_value_validation, test[['Datetime']], validation[['Datetime']])

    print("Tables:")
    returns_table = create_table(data.set_index('Datetime'))
    print(returns_table)

    print("Performance Metrics:")
    metrics = all_metrics(test_val_portfolio)
    print(metrics)

    print(f"Win Rate: {win_rate:.2%}")
    


if __name__ == "__main__":
    main()
