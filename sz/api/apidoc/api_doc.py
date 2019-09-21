from typing import Union

from flask import Blueprint, request
from flask import render_template

import sz
from sz.api.base.api_doc import all_web_api, web_api
from sz.api.base.reply_base import ReplyBase

apidoc = Blueprint('apidoc', __name__, template_folder = 'templates')


@apidoc.route('/api_list')
def api_list():
    apis = all_web_api()
    return render_template('api_list.html',
                           api_list = apis,
                           test_get_path = path_by_func_full_name('sz.api.apidoc.api_doc.test_get'),
                           test_post_path = path_by_func_full_name('sz.api.apidoc.api_doc.test_post'))


@apidoc.route('/test_get')
def test_get():
    api_path = request.args['api_path']
    api = find_api(api_path)
    return render_template('test_get.html', api = api)


def find_api(api_path: str):
    for api in all_web_api():
        if api.path == api_path:
            return api

    return None


@apidoc.route('/test_post')
def test_post():
    api_path = request.args['api_path']
    api = find_api(api_path)
    return render_template('test_post.html', api = api)


@apidoc.route('/api_def_list')
@web_api
def api_def_list() -> ReplyBase:
    """
    返回所有通过 @json_api 定义的api定义
    """
    reply = ReplyBase()
    reply.api_list = all_web_api()
    return reply


def path_by_func_full_name(fullname: str) -> str:
    endpoint = endpoint_of_func(fullname)
    return path_of_endpoint(endpoint)


def endpoint_of_func(fullname: str) -> Union[str, None]:
    for endpoint, func in sz.application.app.view_functions.items():
        func_fullname = '%s.%s' % (func.__module__, func.__qualname__)
        if func_fullname == fullname:
            return endpoint
    return None


def path_of_endpoint(endpoint: str) -> str:
    rules = [rule for rule in sz.application.app.url_map.iter_rules(endpoint = endpoint)]
    return rules[0].rule
