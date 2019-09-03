import glob
from typing import Union, List

import numpy as np
import pandas as pd


def rescaling(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    min-max 归一化：将数值范围缩放到（0,1）,但没有改变数据分布
    """
    max_value = df[column_name].max()
    min_value = df[column_name].min()
    s_rescaling = df[column_name].apply(lambda it: (it - min_value) / (max_value - min_value))
    df[column_name + '_rescaling'] = s_rescaling
    return df


def tushare_date_parser(x):
    item = str(x)
    if item and item != 'nan':
        return pd.datetime.strptime(item, "%Y%m%d")
    else:
        return np.nan


def load_tushare_data(pathname: str,
                      parse_dates: Union[bool, List[str]] = False,
                      date_parser = tushare_date_parser) -> pd.DataFrame:
    file_names = glob.glob(pathname)
    dfs = map(lambda fpath: pd.read_csv(
        fpath, parse_dates = parse_dates, date_parser = date_parser), file_names)
    return pd.concat(dfs)
