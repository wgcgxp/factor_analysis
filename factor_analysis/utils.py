# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def compute_forward_returns(factor,
                            prices,
                            periods=(1, 2, 3)):
    """
    Finds the N period forward returns (as percent change) for each asset
    provided.
    Parameters
    ----------
    factor : pd.Series - MultiIndex
        A MultiIndex Series indexed by timestamp (level 0) and asset
        (level 1), containing the values for a single alpha factor.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    prices : pd.DataFrame
        Pricing data to use in forward price calculation.
        Assets as columns, dates as index. Pricing data must
        span the factor analysis time period plus an additional buffer window
        that is greater than the maximum number of expected periods
        in the forward returns calculations.
    periods : sequence[int]
        periods to compute forward returns on.
    filter_zscore : int or float, optional
        Sets forward returns greater than X standard deviations
        from the the mean to nan. Set it to 'None' to avoid filtering.
        Caution: this outlier filtering incorporates lookahead bias.
    cumulative_returns : bool, optional
        If True, forward returns columns will contain cumulative returns.
        Setting this to False is useful if you want to analyze how predictive
        a factor is for a single forward day.
    Returns
    -------
    forward_returns : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by timestamp (level 0) and asset
        (level 1), containing the forward returns for assets.
        Forward returns column names follow the format accepted by
        pd.Timedelta (e.g. '1D', '30m', '3h15m', '1D1h', etc).
        'date' index freq property (forward_returns.index.levels[0].freq)
        will be set to a trading calendar (pandas DateOffset) inferred
        from the input data (see infer_trading_calendar for more details).
    """

    factor_dateindex = factor.index.levels[0]

    factor_dateindex = factor_dateindex.intersection(prices.index)

    assert(factor_dateindex.size == prices.shape[0])


    raw_values_dict = {}
    column_list = []

    for period in sorted(periods):
        assert(period < factor_dateindex.size)

        returns = prices.pct_change(period)
        forward_returns = returns.shift(-period).reindex(factor_dateindex)

        start, end = forward_returns.index[0], forward_returns.index[0 + period]
        period_len = end - start

        label = timedelta_to_string(period_len, period)
        column_list.append(label)
        raw_values_dict[label] = np.concatenate(forward_returns.values)

    df = pd.DataFrame.from_dict(raw_values_dict)
    df.set_index(
        pd.MultiIndex.from_product(
            [factor_dateindex, prices.columns],
            names=['date', 'asset']
        ),
        inplace=True
    )
    df = df.reindex(factor.index)
    # now set the columns correctly
    df = df[column_list]
    df.index.set_names(['date', 'asset'], inplace=True)

    return df

def timedelta_to_string(timedelta, period):
    """
    Utility that converts a pandas.Timedelta to a string representation
    compatible with pandas.Timedelta constructor format
    Parameters
    ----------
    timedelta: pd.Timedelta
    period: int
    Returns
    -------
    string
        string representation of 'timedelta'
    """
    c = timedelta.components
    format = ''
    if c.days > 400:
        format += '%dY'%(period)
    elif c.days > 80:
        format += '%dQ'%(period)
    elif c.days > 19:
        format += '%dM'%(period)
    else:
        format += '%dD'%(period)
    return format

def hello():
    print("hello world!")
