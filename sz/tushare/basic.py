from functools import lru_cache
from os import path
from typing import Dict

import pandas as pd

import sz
from sz.toolbox.dataframe_tools import load_tushare_data
from sz.toolbox.lazy import lazy_fun
from sz.tushare import data_dir


def load_stock_basic() -> pd.DataFrame:
    pathname = path.join(data_dir, 'stock_basic', '*.csv')
    sz.log_debug('loading: %s' % pathname)
    return load_tushare_data(pathname = pathname)


@lru_cache(maxsize = 1)
def stock_map() -> Dict[str, str]:
    df = load_stock_basic()
    result = {}

    for index, row in df.iterrows():
        ts_code = row['ts_code']
        name = row['name']
        result[ts_code] = name

    return result


def name_of(ts_code: str) -> str:
    return stock_map()[ts_code]


@lazy_fun
def test_cache() -> str:
    sz.log_c_debug('test_cache is called')
    return "sssssssssssss is cached"
