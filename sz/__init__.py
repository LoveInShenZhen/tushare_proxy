from flask import Flask
from sz.api.sample.tmp_test import tmptest
from sz.api.tushare.stocks import tushare
import os
from sz.config import config
from sz import application
import colorama


def create_app():
    colorama.init(autoreset = True)
    application.app = Flask(__name__)

    # todo: register blueprint
    application.app.register_blueprint(tmptest, url_prefix = '/tmp')
    application.app.register_blueprint(tushare, url_prefix = '/tushare')

    return application.app


def setup_app_home(home_path: str):
    application.APP_HOME = os.path.abspath(home_path)
    # load config and setup log level
    application.app.logger.setLevel(config().get_string('logger.level', 'DEBUG'))


def log_debug(msg, *args, **kwargs):
    application.app.logger.debug(msg, *args, **kwargs)


def log_c_debug(msg, *args, **kwargs):
    application.app.logger.debug('%s%s' % (colorama.Fore.BLUE, msg), *args, **kwargs)
