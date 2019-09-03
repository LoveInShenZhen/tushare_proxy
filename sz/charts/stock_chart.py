import jsonpickle
import pandas as pd
from datetime import datetime
from sz.charts import jinja_env


def ohlc_of_bar_df(df: pd.DataFrame) -> str:
    """
    将 pro_bar 的 dataFrame 转换成 highstock 中 ohlc 所需的形式
    参考1: https://tushare.pro/document/2?doc_id=109
    参考2: https://api.highcharts.com.cn/highstock#series%3Cohlc%3E.data
    :param df:
    :return:
    """
    # for index, row in df.iterrows():
    #     print('index: %s, row: %s\n' % (index, row))

    ohlc_data = []
    for index, row in df.sort_values(by = ['trade_date']).iterrows():
        trade_date = int(datetime.strptime('%s 09:00:00' % row['trade_date'], '%Y%m%d %H:%M:%S').timestamp() * 1000)
        # [date,open,high,low,close]
        ohlc_data.append([trade_date, row['open'], row['high'], row['low'], row['close']])

    return jsonpickle.encode(ohlc_data, unpicklable = False, use_decimal = True)


def volume_of_bar_df(df: pd.DataFrame) -> str:
    volume = []
    for index, row in df.sort_values(by = ['trade_date']).iterrows():
        trade_date = int(datetime.strptime('%s 09:00:00' % row['trade_date'], '%Y%m%d %H:%M:%S').timestamp() * 1000)
        volume.append([trade_date, row['vol']])

    return jsonpickle.encode(volume, unpicklable = False, use_decimal = True)


def output_html(df: pd.DataFrame, stock_name: str, adj_type: str) -> str:
    data = {
        'ohlc_data': ohlc_of_bar_df(df),
        'volume_data': volume_of_bar_df(df),
        'stock_name': stock_name,
        'adj_type': adj_type
    }
    template = jinja_env.get_template('stock_chart.html')
    return template.render(data)
