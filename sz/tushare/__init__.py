import tushare as ts

from sz.config import config

data_dir = config().get_string('tushare.data_dir')


def ts_pro_api():
    return ts.pro_api(config().get_string('tushare.token'))
