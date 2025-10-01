from models import Operation

def get_portfolio_value(cash: float, long_ops: list[Operation], short_ops: list[Operation], current_price: float, n_shares: int, COM: float) -> float:
    val = cash

    for position in long_ops:
        val += row.Close * position.n_shares * (1 - COM)

    for position in short_ops:
        profit_losses = (position.price - row.Close) * position.n_shares *(1-COM)
        val += (position.n_shares * position.n_shares * (1 + COM)) + profit_losses

    return val

