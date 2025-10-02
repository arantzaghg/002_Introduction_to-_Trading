from models import Operation
import pandas as pd

def get_portfolio_value(cash: float, long_ops: list[Operation], short_ops: list[Operation], current_price: float, n_shares: int, COM: float) -> float:
    val = cash

    for position in long_ops:
        val += current_price * position.n_shares * (1 - COM)

    for position in short_ops:
        profit_losses = (position.price - current_price) * position.n_shares *(1-COM)
        val += (position.n_shares * position.n_shares * (1 + COM)) + profit_losses

    return val

def split_fun(data: pd.DataFrame):
    train_size = int(len(data) * 0.6)
    test_size = int(len(data) * 0.2)
    train = data[:train_size]
    test = data[train_size:train_size + test_size]
    validation = data[train_size + test_size:]

    return train, test, validation

