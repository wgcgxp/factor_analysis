import pandas as pd
import numpy as np
import datetime as dt
import factor_analysis as fa

index_code = 'CI005016.WI' # 中信家电
start_date, end_date = '2009-12-31', '2020-9-30'

def main():
    stocks = fa.data.get_stock_list(index_code)
    prices = fa.data.get_stocks_history_close(stocks['wind_code'].tolist(), start_date, end_date, period='Q')
    # 去掉区间之内上市的股票
    prices = prices.dropna(axis=1)
    # factor = fa.data.get_stocks_fundamental_factor(prices.columns.tolist(), 'roe', start_date, end_date)
    factor = fa.data.get_stocks_fundamental_factor(prices.columns.tolist(), 'grossprofitmargin', start_date, end_date)
    factor.index.set_names(['date'], inplace=True)
    factor = factor.stack()
    factor.index.set_names(['date', 'asset'], inplace=True)
    factor_data = fa.utils.get_clean_factor_and_forward_returns(factor, prices, periods=(1,2,3))
    fa.tears.create_returns_tear_sheet(factor_data)

if __name__ == '__main__':
    main()