from models import Operation

def get_portfolio_value(cash: float, long_ops: list[Operation], short_ops: list[Operation], current_price: float, n_shares: int, COM: float) -> float:
    val = cash

    for long_position in long_ops:
        val += current_price * long_position.n_shares * (1 - COM)

    for short_position in short_ops:
        profit_losses = (short_position.price - current_price) * short_position.n_shares *(1-COM)
        val += (short_position.n_shares * short_position.n_shares * (1 + COM)) + profit_losses

    return val

