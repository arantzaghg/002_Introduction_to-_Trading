import pandas as pd
import matplotlib.pyplot as plt

## CAMBIAR 



def port_val(portfolio_values):
    plt.figure(figsize=(10, 5))
    plt.plot(portfolio_values, color='rosybrown')
    plt.title('Portfolio value through time (train)')
    plt.grid()
    plt.show()


def test_val(test_portfolio, validation_portfolio, test, validation):
    df_test = pd.DataFrame({'Date': test['Datetime'].reset_index(drop=True), 'Portfolio Value': test_portfolio})
    df_validation = pd.DataFrame({'Date': validation['Datetime'].reset_index(drop=True), 'Portfolio Value': validation_portfolio})

    plt.figure(figsize=(10, 5))
    plt.plot(df_test['Date'], df_test['Portfolio Value'], label='Test', color='rosybrown')
    plt.plot(df_validation['Date'], df_validation['Portfolio Value'], label='Validation', color='cornflowerblue')
    plt.title('Test & Validation value through time ')
    plt.xlabel('Time')
    plt.ylabel('Portfolio value')
    plt.legend()
    plt.grid()
    plt.show()

   