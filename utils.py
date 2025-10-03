from models import Operation
import pandas as pd

def get_portfolio_value(cash: float, long_ops: list[Operation], short_ops: list[Operation], current_price: float, n_shares: float) -> float:
    portfolio_value = cash 
    for position in long_ops:
        portfolio_value += position.n_shares * current_price

    for position in short_ops:
        profit_loss = ((position.price - current_price) * position.n_shares)
        portfolio_value += (position.n_shares * position.price) + profit_loss
    return portfolio_value

def split_fun(data: pd.DataFrame):
    train_size = int(len(data) * 0.6)
    test_size = int(len(data) * 0.2)
    train = data[:train_size]
    test = data[train_size:train_size + test_size]
    validation = data[train_size + test_size:]

    return train, test, validation

