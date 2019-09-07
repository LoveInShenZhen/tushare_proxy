from flask import Blueprint
from sz.api.base.api_doc import all_json_api
from flask import render_template

apidoc = Blueprint('apidoc', __name__, template_folder = 'templates')


@apidoc.route('/api_list')
def api_list():
    apis = all_json_api()
    return render_template('api_list.html', api_list=apis)
