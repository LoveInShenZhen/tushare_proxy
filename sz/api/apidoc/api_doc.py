from flask import Blueprint, request
from sz.api.base.api_doc import all_json_api
from flask import render_template
import sz
import jsonpickle

apidoc = Blueprint('apidoc', __name__, template_folder = 'templates')


@apidoc.route('/api_list')
def api_list():
    apis = all_json_api()
    return render_template('api_list.html', api_list = apis)


@apidoc.route('/test_get')
def test_get():
    api_path = request.args['api_path']
    api = find_api(api_path)
    return render_template('test_get.html', api = api)


def find_api(api_path: str):
    for api in all_json_api():
        if api.path == api_path:
            return api

    return None

@apidoc.route('/test_post')
def test_post():
    api_path = request.args['api_path']
    api = find_api(api_path)
    return render_template('test_post.html', api = api)
