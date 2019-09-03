import os

from pyhocon import ConfigFactory, ConfigTree

from sz import application

__config__ = None


def config() -> ConfigTree:
    global __config__
    if __config__ is None:
        __config__ = ConfigFactory.parse_file(os.path.join(application.APP_HOME, 'conf', 'application.conf'))

    return __config__
