from flask import Flask
from sz.api.sample.tmp_test import tmptest
from sz.api.tushare.stocks import tushare
from sz.api.apidoc.api_doc import apidoc
import os
from sz.config import config
from sz import application
import colorama


def create_app():
    colorama.init(autoreset = True)
    application.app = Flask(__name__)
    application.logger().setLevel('DEBUG')

    # todo: register blueprint
    application.app.register_blueprint(apidoc, url_prefix='/doc')
    application.app.register_blueprint(tmptest, url_prefix = '/tmp')
    application.app.register_blueprint(tushare, url_prefix = '/tushare')

    log_c_debug('api list: http://localhost:5000/doc/api_list')

    return application.app


def setup_app_home(home_path: str):
    application.APP_HOME = os.path.abspath(home_path)
    # load config and setup log level
    application.logger().setLevel(config().get_string('logger.level', 'DEBUG'))


def log_debug(msg, *args, **kwargs):
    application.logger().debug(msg, *args, **kwargs)


def log_c_debug(msg, *args, **kwargs):
    application.logger().debug('%s%s' % (colorama.Fore.BLUE, msg), *args, **kwargs)
