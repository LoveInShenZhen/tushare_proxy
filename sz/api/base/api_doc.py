import inspect
from functools import update_wrapper

import flask

from sz.api.base.reply_base import json_response


def json_api(func):
    """
    json_api 装饰器, 它应该处于 flask route 装饰器的下面
    :param func: 被装饰器所包装的函数方法
    :return: 返回包装后的函数方法
    """

    def wrapper(*args, **kwds):
        request = flask.request
        arg_spec = inspect.getfullargspec(func)
        for arg in arg_spec.args:
            arg_value = request.args.get(arg)
            if arg_value is not None:
                kwds[arg] = arg_value
        # sz.log_debug(Fore.BLUE + 'args: %s,' % (str(inspect.getfullargspec(func))))
        reply = func(*args, **kwds)
        return json_response(reply)

    return update_wrapper(wrapper, func)


class ApiRoute(object):

    def __init__(self, api_path: str, ):
        self.api_path = api_path
