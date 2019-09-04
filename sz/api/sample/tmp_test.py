import os

import flask
from flask import Blueprint, Request

import sz
from sz import application
from sz.api.base.api_doc import json_api
from sz.api.base.reply_base import ReplyBase, json_response
from sz.config import config
from sz.tushare.basic import test_cache

tmp_test = Blueprint('tmp_test', __name__)
request: Request = flask.request


@tmp_test.route('/test')
def test():
    reply = ReplyBase()
    reply.greetings = '老板好! 恭喜老板发财! 夜夜嫩模! 一夜七次! 一次一小时!'
    sz.log_debug('\n%s', reply.json_str())
    return json_response(reply)


@tmp_test.route('/reply_test')
def reply_test():
    reply = ReplyBase()
    reply.greetings = '你好! 恭喜老板发财! 夜夜嫩模!'
    return json_response(reply)


@tmp_test.route('/current_path')
def current_path():
    reply = ReplyBase()
    reply.current_path = os.path.abspath('.')
    return json_response(reply)


@tmp_test.route('/app_home')
def app_home():
    reply = ReplyBase()
    reply.app_home = application.APP_HOME
    return json_response(reply)


@tmp_test.route('/config_path')
def config_path():
    reply = ReplyBase()
    reply.config_path = os.path.join(application.APP_HOME, 'conf', 'application.conf')
    return json_response(reply)


@tmp_test.route('/read_config')
def read_config():
    cfg_key = request.args['config']
    reply = ReplyBase()
    reply.config_path = config
    reply.config_value = config().get_string(cfg_key, "undefined")
    return json_response(reply)


@tmp_test.route('/url_map')
def url_map():
    """
    url_map 的文档
    :return:
    """
    reply = ReplyBase()
    reply.url_map = str(application.app.url_map)
    sz.log_debug(type(application.app.url_map))
    # for rule in application.app.url_map.iter_rules():
    #     sz.log_debug('rule: %s, endpoin: %s, endpoint_type: %s' % (rule, rule.endpoint, type(rule.endpoint)))
    rules = list(application.app.url_map.iter_rules())
    sz.log_c_debug('rule type: %s' % type(rules[0]))
    rule = rules[0]
    sz.log_c_debug('rule path: %s, methods: %s, endpoint: %s' % (rule.rule, rule.methods, rule.endpoint))

    # for (k, v) in application.app.view_functions.items():
    #     print('%s : %s, name: %s' % (k, type(v), v.__name__))

    return json_response(reply)


@tmp_test.route('/api_doc')
@json_api
def api_doc(api_path: str = 'undefined', tag: str = '') -> ReplyBase:
    """
    api_doc 接口文档
    :param tag:
    :param api_path:
    :return:
    """
    reply = ReplyBase()
    reply.api_path = api_path
    reply.tag = tag
    return reply
