import os
from typing import List, Iterable

import pandas as pd
import tushare as ts

from sz.config import config
from sz.tushare import ts_pro_api


def bar_data(ts_code: str = '',
             start_date: str = '',
             end_date: str = '',
             freq: str = 'D',
             asset: str = 'E',
             adj: str = None,
             ma: List[int] = [],
             factors: List[str] = None,
             retry_count: int = 3) -> pd.DataFrame:
    """
    通用行情接口, BAR 数据
    Parameters:
    ------------
    ts_code:证券代码，支持股票,ETF/LOF,期货/期权,港股,数字货币
    start_date:开始日期  YYYYMMDD
    end_date:结束日期 YYYYMMDD
    freq:支持分钟(min)/日(D)/周(W)/月(M)K线，其中1min表示1分钟（类推1/5/15/30/60分钟） ，默认D
    asset:证券类型 E:股票和交易所基金，I:沪深指数,C:数字货币,FT:期货 FD:基金/O期权/H港股/CB可转债
    adj:复权类型,None不复权,qfq:前复权,hfq:后复权
    ma:均线,支持自定义均线频度，如：ma5/ma10/ma20/ma60/maN
    factors因子数据，目前支持以下两种：
        vr:量比,默认不返回，返回需指定：factor=['vr']
        tor:换手率，默认不返回，返回需指定：factor=['tor']
                    以上两种都需要：factor=['vr', 'tor']
    retry_count:网络重试次数
    """
    api = ts_pro_api()

    cache_path = cache_file_path(ts_code, start_date, end_date, freq, asset, adj, ma, factors)
    if os.path.exists(cache_path):
        return pd.read_csv(cache_path).round({
            'open': 2,
            'high': 2,
            'low': 2,
            'close': 2,
            'pre_close': 2,
            'change': 2,
            'pct_chg': 2,
            'vol': 4,
            'amount': 4
        })

    df: pd.DataFrame = ts.pro_bar(ts_code = ts_code,
                                  api = api,
                                  start_date = start_date,
                                  end_date = end_date,
                                  freq = freq,
                                  asset = asset,
                                  adj = adj,
                                  ma = ma,
                                  factors = factors,
                                  retry_count = retry_count)

    cache_folder = cache_dir()
    if not os.path.exists(cache_dir()):
        os.makedirs(cache_folder)

    df.to_csv(cache_path, index = False)

    return df


def cache_file_name(ts_code: str,
                    start_date: str,
                    end_date: str,
                    freq: str,
                    asset: str,
                    adj: str,
                    ma: List[int],
                    factors: List[str]) -> str:
    paramap = {
        'ts_code': __empty_as_none__(ts_code),
        'start_date': __empty_as_none__(start_date),
        'end_date': __empty_as_none__(end_date),
        'freq': __empty_as_none__(freq),
        'asset': __empty_as_none__(asset),
        'adj': __empty_as_none__(adj),
        'ma': __sorted_list_as_str__(ma),
        'factors': __sorted_list_as_str__(factors)
    }
    return '{ts_code}_{start_date}_{end_date}_{freq}_{asset}_{adj}_{ma}_{factors}.csv'.format_map(paramap)


def cache_file_path(ts_code: str,
                    start_date: str,
                    end_date: str,
                    freq: str,
                    asset: str,
                    adj: str,
                    ma: List[int],
                    factors: List[str]) -> str:
    """
    返回缓存文件的路径
    :param ts_code:
    :param start_date:
    :param end_date:
    :param freq:
    :param asset:
    :param adj:
    :param ma:
    :param factors:
    :return:
    """
    file_name = cache_file_name(ts_code, start_date, end_date, freq, asset, adj, ma, factors)
    return os.path.join(cache_dir(), file_name)


def cache_dir() -> str:
    """
    返回缓存文件存放的目录
    :return:
    """
    return os.path.join(config().get_string('tushare.data_dir'), 'pro_bar')


def __empty_as_none__(s: str) -> str:
    if s is None:
        return 'None'
    elif len(s.strip()) == 0:
        return 'None'
    else:
        return s


def __sorted_list_as_str__(iterable: Iterable) -> str:
    if iterable is None:
        return 'None'
    else:
        sorted_list = sorted(iterable)
        if len(sorted_list) == 0:
            return 'None'
        else:
            return '|'.join(sorted_list)
