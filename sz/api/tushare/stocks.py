from datetime import datetime
from typing import List

import flask
import pandas as pd
from flask import Blueprint, Request

import sz
from sz.api.base.reply_base import ReplyBase, json_response
from sz.tushare.basic import name_of
from sz.tushare.pro_bar import bar_data
from sz.charts.stock_chart import output_html

tushare = Blueprint('tushare', __name__)
request: Request = flask.request


def name_of_adj(adj: str) -> str:
    adj_map = {
        '': '不复权',
        None: '不复权',
        'qfq': '前复权',
        'hfq': '后复权'
    }
    return adj_map[adj]


@tushare.route('/stock_chart')
def stock_chart():
    df = stock_df()
    ts_code = request.args['ts_code']
    adj = request.args.get('adj', default = None)
    stock_name = name_of(ts_code = ts_code)
    adj_name = name_of_adj(adj)
    response = flask.make_response(output_html(df = df, stock_name = stock_name, adj_type = adj_name))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


@tushare.route('/stock_csv')
def stock_csv():
    df = stock_df()
    response = flask.make_response(df.to_csv(index = False))
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


def stock_df() -> pd.DataFrame:
    ts_code = request.args['ts_code']
    start_date = request.args.get('start_date', '20160101')
    end_date = request.args.get('end_date', datetime.today().strftime('%Y%m%d'))
    freq = request.args.get('freq', default = 'D')
    asset = request.args.get('asset', default = 'E')
    adj = request.args.get('adj', default = None)
    ma = _drop_blank(request.args.get('ma', default = '').split(','))
    factors = _drop_blank(request.args.get('factors', default = '').split(','))

    sz.log_debug('ma: %s', ma)
    sz.log_debug('factors: %s', factors)

    return bar_data(ts_code = ts_code,
                    start_date = start_date,
                    end_date = end_date,
                    freq = freq,
                    asset = asset,
                    adj = adj,
                    ma = ma,
                    factors = factors)


def _drop_blank(str_list: List[str]) -> List[str]:
    return [it for it in str_list if len(it) > 0]


@tushare.route('/name_by_code')
def name_by_code():
    ts_code = request.args['ts_code']
    name = name_of(ts_code = ts_code)
    reply = ReplyBase()
    reply.name = name
    return json_response(reply)
