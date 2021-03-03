import pandas as pd
import numpy as np
import datetime as dt
from WindPy import w

w.start()

today = dt.datetime.today().strftime('%Y-%m-%d')

def get_stock_list(index_code):
    data = w.wset("sectorconstituent", "date=%s;windcode=%s;field=wind_code,sec_name"%(today, index_code))
    df = pd.DataFrame(data.Data, index=data.Fields).T
    return df

def get_stocks_history_close(codes, start_date, end_date, period):
    if period in ['M', 'Q']:
        data = w.wsd(codes, 'close', start_date, end_date, 'Period=%s;Days=Alldays'%(period))
        df = pd.DataFrame(data.Data, index=data.Codes, columns=pd.to_datetime(data.Times)).T
    return df

def get_stocks_fundamental_factor(codes, factor_name, start_date, end_date):
    data = w.wsd(codes, factor_name, start_date, end_date, "Period=Q;Days=Alldays")
    df = pd.DataFrame(data.Data, index=data.Codes, columns=pd.to_datetime(data.Times)).T
    return df