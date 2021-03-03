import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd

from . import plotting
from . import performance as perf
from . import utils

class GridFigure(object):
    """
    It makes life easier with grid plots
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.fig = plt.figure(figsize=(14, rows * 7))
        self.gs = gridspec.GridSpec(rows, cols, wspace=0.4, hspace=0.3)
        self.curr_row = 0
        self.curr_col = 0

    def next_row(self):
        if self.curr_col != 0:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, :])
        self.curr_row += 1
        return subplt

    def next_cell(self):
        if self.curr_col >= self.cols:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, self.curr_col])
        self.curr_col += 1
        return subplt

    def close(self):
        plt.close(self.fig)
        self.fig = None
        self.gs = None

def create_returns_tear_sheet(
    factor_data, long_short=True, group_neutral=False, by_group=False
):
    """
    Creates a tear sheet for returns analysis of a factor.
    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to,
        and (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    long_short : bool
        Should this computation happen on a long short portfolio? if so, then
        mean quantile returns will be demeaned across the factor universe.
        Additionally factor values will be demeaned across the factor universe
        when factor weighting the portfolio for cumulative returns plots
    group_neutral : bool
        Should this computation happen on a group neutral portfolio? if so,
        returns demeaning will occur on the group level.
        Additionally each group will weight the same in cumulative returns
        plots
    by_group : bool
        If True, display graphs separately for each group.
    """

    factor_returns = perf.factor_returns(
        factor_data, long_short, group_neutral
    )

    mean_quant_ret, std_quantile = perf.mean_return_by_quantile(
        factor_data,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
        factor_data,
        by_date=True,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    vertical_sections = 3
    gf = GridFigure(rows=vertical_sections, cols=1)

    plotting.plot_quantile_returns_bar(
        mean_quant_ret,
        by_group=False,
        ylim_percentiles=None,
        ax=gf.next_row(),
    )

    first_col = factor_returns.columns[0]
    title = (
        "Factor Weighted "
        + ("行业中性 " if group_neutral else "")
        + ("多空 " if long_short else "")
        + "组合累积收益率 (%s)"
    )%(first_col)
    plotting.plot_cumulative_returns(
        factor_returns, period=first_col, title=title, ax=gf.next_row()
    )

    plotting.plot_cumulative_returns_by_quantile(
        mean_quant_ret_bydate, period=first_col, ax=gf.next_row()
    )

    plt.show()
    gf.close()