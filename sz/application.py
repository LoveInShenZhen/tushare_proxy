import os
from flask import Flask
from logging import Logger

APP_HOME = os.path.abspath('.')

app: Flask = None


def logger() -> Logger:
    return app.logger
