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
    study.optimize(lambda trial: optimize(trial, train), n_trials=50)

    print("Best Parameters:", study.best_params)
    print("Best Value:", study.best_value)


    train_data = get_signal(train.copy(), study.best_params)
    portfolio_value_train, win_rate_train, c_test = backtestings(train_data, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'], cash = 1_000_000)

    test_data = get_signal(test.copy(), study.best_params)
    portfolio_value_test, win_rate_test, c_train= backtestings(test_data, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'], cash = 1_000_000)
    
    validation_data = get_signal(validation.copy(), study.best_params)
    portfolio_value_validation, win_rate_validation, c_validation = backtestings(validation_data, study.best_params['stop_loss'], study.best_params['take_profit'], study.best_params['n_shares'], cash = c_test)

    combined = pd.concat([test_data, validation_data]).reset_index(drop=True)
    complete_port = portfolio_value_test + portfolio_value_validation   

    # PROBABLEMENTE FALTA SHIFT
    port_val(portfolio_value_train)
    test_val(portfolio_value_test, portfolio_value_validation, test[['Datetime']], validation[['Datetime']])        
    
    print("Performance Summary:")
    print(f"Final Cash (Train): ${c_test:,.2f}")
    print(f"Portfolio Value (Train): ${portfolio_value_train.iloc[-1]:,.2f}")
    print(f"Win Rate (Train): {win_rate_train:.2%}")
    print(f"Metrics (Train): {all_metrics(portfolio_value_train)}")
    print(f"Returns (Train): {portfolio_value_train, train_data}")

    print(f"Final Cash (Test): ${c_train:,.2f}")
    print(f"Portfolio Value (Test): ${portfolio_value_test.iloc[-1]:,.2f}")
    print(f"Win Rate (Test): {win_rate_test:.2%}")
    print(f"Metrics (Test): {all_metrics(portfolio_value_test)}")
    print(f"Returns (Test): {portfolio_value_test, test_data}")
    
    print(f"Final Cash (Validation): ${c_validation:,.2f}")
    print(f"Portfolio Value (Validation): ${portfolio_value_validation.iloc[-1]:,.2f}")
    print(f"Win Rate (Validation): {win_rate_validation:.2%}")
    print(f"Metrics (Validation): {all_metrics(portfolio_value_validation)}")
    print(f"Returns (Validation): {portfolio_value_validation, validation_data}")

    print(f"Final Cash (Complete): ${c_validation:,.2f}")
    print(f"Portfolio Value (Complete): ${complete_port.iloc[-1]:,.2f}")
    print(f"Metrics (Complete): {all_metrics(complete_port)}")
    print(f"Returns (Complete): {complete_port, combined}")


    #print("Tables:")
    #returns_table = create_table(data.set_index('Datetime'))
    #print(returns_table)

if __name__ == "__main__":
    main()
