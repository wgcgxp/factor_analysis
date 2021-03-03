import numpy as np
import pandas as pd

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from . import utils
from . import performance as perf

def plot_quantile_returns_bar(mean_ret_by_q,
                              by_group=False,
                              ylim_percentiles=None,
                              ax=None):
    """
    Plots mean period wise returns for factor quantiles.
    Parameters
    ----------
    mean_ret_by_q : pd.DataFrame
        DataFrame with quantile, (group) and mean period wise return values.
    by_group : bool
        Disaggregated figures by group.
    ylim_percentiles : tuple of integers
        Percentiles of observed data to use as y limits for plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    mean_ret_by_q = mean_ret_by_q.copy()

    if ylim_percentiles is not None:
        ymin = (np.nanpercentile(mean_ret_by_q.values,
                                 ylim_percentiles[0]))
        ymax = (np.nanpercentile(mean_ret_by_q.values,
                                 ylim_percentiles[1]))
    else:
        ymin = None
        ymax = None

    if by_group:
        num_group = len(
            mean_ret_by_q.index.get_level_values('group').unique())

        if ax is None:
            v_spaces = ((num_group - 1) // 2) + 1
            f, ax = plt.subplots(v_spaces, 2, sharex=False,
                                 sharey=True, figsize=(16, 9 * v_spaces))
            ax = ax.flatten()

        for a, (sc, cor) in zip(ax, mean_ret_by_q.groupby(level='group')):
            (cor.xs(sc, level='group')
                .plot(kind='bar', title=sc, ax=a))

            a.set(xlabel='', ylim=(ymin, ymax))
            a.set_ylabel('均值收益率', fontsize=15)
            vals = ax.get_yticks()
            a.set_yticklabels(['{:2.0f}%'.format(x*100) for x in vals])

        if num_group < len(ax):
            ax[-1].set_visible(False)

        return ax

    else:
        if ax is None:
            f, ax = plt.subplots(1, 1, figsize=(16, 9))

        (mean_ret_by_q.plot(kind='bar', ax=ax))
        ax.set_title('分组分期限均值收益率', fontsize=20)
        ax.set(xlabel='', ylim=(ymin, ymax))
        ax.set_ylabel('均值收益率', fontsize=15)
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:2.1f}%'.format(x*100) for x in vals])

        return ax

def plot_cumulative_returns_by_quantile(quantile_returns,
                                        period,
                                        freq=None,
                                        ax=None):
    """
    Plots the cumulative returns of various factor quantiles.
    Parameters
    ----------
    quantile_returns : pd.DataFrame
        Returns by factor quantile
    period : pandas.Timedelta or string
        Length of period for which the returns are computed (e.g. 1 day)
        if 'period' is a string it must follow pandas.Timedelta constructor
        format (e.g. '1 days', '1D', '30m', '3h', '1D1h', etc)
    freq : pandas DateOffset
        Used to specify a particular trading calendar e.g. BusinessDay or Day
        Usually this is inferred from utils.infer_trading_calendar, which is
        called by either get_clean_factor_and_forward_returns or
        compute_forward_returns
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    Returns
    -------
    ax : matplotlib.Axes
    """

    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(16, 9))

    assert(period in quantile_returns.columns)
    ret_wide = quantile_returns[period].unstack('factor_quantile')

    cum_ret = ret_wide.apply(perf.cumulative_returns)

    cum_ret = cum_ret.loc[:, ::-1]  # we want negative quantiles as 'red'

    cum_ret.plot(lw=2, ax=ax, cmap=cm.coolwarm)
    ax.legend()
    ymin, ymax = cum_ret.min().min(), cum_ret.max().max()
    ax.set(xlabel='',
           yscale='symlog',
           yticks=np.linspace(ymin, ymax, 5),
           ylim=(ymin, ymax))

    ax.set_title('''分组累积收益率 ({})'''.format(period), fontsize=20)
    ax.set_ylabel('对数累积收益率', fontsize=15)

    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.axhline(1.0, linestyle='-', color='black', lw=1)

    return ax

def plot_cumulative_returns(factor_returns,
                            period,
                            freq=None,
                            title=None,
                            ax=None):
    """
    Plots the cumulative returns of the returns series passed in.
    Parameters
    ----------
    factor_returns : pd.Series
        Period wise returns of dollar neutral portfolio weighted by factor
        value.
    period : pandas.Timedelta or string
        Length of period for which the returns are computed (e.g. 1 day)
        if 'period' is a string it must follow pandas.Timedelta constructor
        format (e.g. '1 days', '1D', '30m', '3h', '1D1h', etc)
    freq : pandas DateOffset
        Used to specify a particular trading calendar e.g. BusinessDay or Day
        Usually this is inferred from utils.infer_trading_calendar, which is
        called by either get_clean_factor_and_forward_returns or
        compute_forward_returns
    title: string, optional
        Custom title
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(16, 9))

    assert(period in factor_returns.columns)
    factor_returns = perf.cumulative_returns(factor_returns[period])

    factor_returns.plot(ax=ax, lw=3, color='forestgreen', alpha=0.6)
    ax.set(xlabel='')
    ax.set_ylabel('累积收益率', fontsize=15)
    ax.set_title("因子组合累积收益率 ({})".format(period) 
                 if title is None else title, fontsize=20)

    ax.axhline(1.0, linestyle='-', color='black', lw=1)
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:2.1f}%'.format(x*100) for x in vals])

    return ax