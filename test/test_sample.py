import pandas as pd
import numpy as np
import datetime as dt
import factor_analysis as fa

def main():
    DATA_DIR = 'D:/workspace/factor_analysis/data'
    factor = pd.read_excel('%s/factor.xlsx'%(DATA_DIR), index_col=0)
    factor.index.set_names(['date'], inplace=True)
    factor = factor.stack()
    factor.index.set_names(['date', 'asset'], inplace=True)
    prices = pd.read_excel('%s/prices.xlsx'%(DATA_DIR), index_col=0)
    factor_data = fa.utils.get_clean_factor_and_forward_returns(factor, prices, periods=(1,2,3))
    fa.tears.create_returns_tear_sheet(factor_data)

if __name__ == '__main__':
    main()