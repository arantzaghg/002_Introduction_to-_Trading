import pandas as pd

def create_table(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    data['Returns'] = data['Close'].pct_change().fillna(0)

    m_returns = data['Returns'].resample('M').apply(lambda x: (1+x).prod() - 1)
    q_returns = data['Returns'].resample('Q').apply(lambda x: (1+x).prod() - 1)
    a_returns = data['Returns'].resample('Y').apply(lambda x: (1+x).prod() - 1)

    df_returns = pd.DataFrame({'Monthly Returns': m_returns, 'Quarterly Returns': q_returns, 'Annual Returns': a_returns})

    return df_returns
