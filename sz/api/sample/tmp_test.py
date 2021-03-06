import inspect
import os
from datetime import datetime

import flask
from flask import Blueprint, Request

import sz
from sz import application
from sz.api.base.api_doc import web_api, all_web_api, WebApiFunc
from sz.api.base.errors import ApiError
from sz.api.base.reply_base import ReplyBase
from sz.config import config

tmptest = Blueprint('tmp_test', __name__)
request: Request = flask.request


@tmptest.route('/test')
@web_api
def test() -> ReplyBase:
    reply = ReplyBase()
    reply.greetings = '老板好! 恭喜老板发财! 夜夜嫩模! 一夜七次! 一次一小时!'
    sz.log_debug('\n%s', reply.json_str())
    return reply


@tmptest.route('/reply_test')
@web_api
def reply_test() -> ReplyBase:
    reply = ReplyBase()
    reply.greetings = '你好! 恭喜老板发财! 夜夜嫩模!'
    return reply


@tmptest.route('/current_path')
@web_api
def current_path() -> ReplyBase:
    reply = ReplyBase()
    reply.current_path = os.path.abspath('.')
    return reply


@tmptest.route('/app_home')
@web_api
def app_home() -> ReplyBase:
    reply = ReplyBase()
    reply.app_home = application.APP_HOME
    return reply


@tmptest.route('/config_path')
@web_api
def config_path() -> ReplyBase:
    reply = ReplyBase()
    reply.config_path = os.path.join(application.APP_HOME, 'conf', 'application.conf')
    return reply


@tmptest.route('/read_config')
@web_api
def read_config(config_path: str) -> ReplyBase:
    """
    读取配置文件中, 指定配置路径(config_path)的配置
    :param config_path: 配置路径
    """
    reply = ReplyBase()
    reply.config_path = config
    reply.config_value = config().get_string(config_path, "undefined")
    return reply


@tmptest.route('/url_map', methods = ['GET', 'POST'])
@web_api
def url_map() -> ReplyBase:
    """
    列出所有的 json api 信息
    :return:
    """
    reply = ReplyBase()
    # reply.url_map = ['%s : %s : %s : %s' % (
    #     rule.rule,
    #     rule.endpoint,
    #     func_name_by_endpoint(rule.endpoint),
    #     comments_by_endpoint(rule.endpoint)) for rule in
    #                  application.app.url_map.iter_rules()]
    # sz.log_c_debug('url_map type: %s', type(application.app.url_map))
    # sz.log_debug(type(application.app.url_map))
    # for rule in application.app.url_map.iter_rules():
    #     sz.log_debug('rule: %s, endpoin: %s, endpoint_type: %s' % (rule, rule.endpoint, type(rule.endpoint)))
    # rules = list(application.app.url_map.iter_rules())
    # sz.log_c_debug('rule type: %s' % type(rules[0]))
    # rule = rules[0]
    # sz.log_c_debug('rule path: %s, methods: %s, endpoint: %s' % (rule.rule, rule.methods, rule.endpoint))

    # for rule in application.app.url_map.iter_rules(endpoint = 'tmp_test.api_doc'):
    #     func = application.app.view_functions[rule.endpoint]
    #     if hasattr(func, '__original__fun__'):
    #         sz.log_c_debug('found __original__fun__')
    #         arg_spec = inspect.getfullargspec(func.__original__fun__)
    #     else:
    #         arg_spec = inspect.getfullargspec(func)
    #     sz.log_c_debug('endpoint:%s, rule: %s, func: %s -- %s',
    #                    rule.endpoint,
    #                    rule.rule,
    #                    fullname_of_func(func),
    #                    str(arg_spec)
    #                    )

    reply.api_list = all_web_api()
    reply.form_data = request.form
    reply.header = {k: v for k, v in request.headers.items()}

    # for (k, v) in application.app.view_functions.items():
    #     print('%s : %s, name: %s' % (k, type(v), v.__name__))

    # modname = 'sz.api.sample.tmp_test'
    # modname = 'flask.helpers'
    # fun_module = importlib.import_module(modname)
    # # sz.log_c_debug('mod type: %s', type(fun_module))
    # # sz.log_c_debug('dir mod: %s', dir(fun_module))
    # sz.log_c_debug('is module: %s', inspect.ismodule(fun_module))
    # sz.log_c_debug('members:')
    # for m in inspect.getmembers(fun_module):
    #     sz.log_c_debug('%s', m)

    return reply


def func_name_by_endpoint(endpoint: str) -> str:
    func = application.app.view_functions[endpoint]
    return '%s.%s' % (func.__module__, func.__qualname__)


def fullname_of_func(func) -> str:
    return '%s.%s' % (func.__module__, func.__qualname__)


def comments_by_endpoint(endpoint: str) -> str:
    x = application.app.view_functions[endpoint]
    return inspect.getcomments(x)


@tmptest.route('/api_doc')
@web_api
def api_doc(api_path: str = '/api/tmp/api_doc', tag: str = 'doc', age: int = 16) -> ReplyBase:
    """
    api_doc 接口文档
    :param age:
    :param tag:
    :param api_path:
    :return:
    """
    reply = ReplyBase()
    reply.api_path = api_path
    reply.tag = tag
    reply.app_debug = application.app.debug
    reply.age = age
    if tag == 'error':
        raise ApiError('模拟异常发生')
    return reply


@tmptest.route('/say_hello')
@web_api
def say_hello(user: str) -> ReplyBase:
    """
    对访问用户打招呼,说 hello, 告诉今天日期
    :param user: 用户名称
    :return: 问候语
    """
    reply = ReplyBase()
    reply.txt = 'Hello %s, today is %s' % (user, datetime.now().strftime('%Y-%m-%d %A'))
    return reply


@tmptest.route('/test_ex')
@web_api
def test_ex(msg: str = 'hello') -> ReplyBase:
    """
    模拟异常产生
    :return:
    """
    raise Exception("模拟代码中异常产生 %s" % msg)
