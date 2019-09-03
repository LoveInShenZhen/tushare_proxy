#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from gevent.pywsgi import WSGIServer
import os
import sz

app = sz.create_app()

sz.setup_app_home(os.path.dirname(__file__))


def start():
    port = 5000
    http_server = WSGIServer(('', port), app)
    app.logger.info('start server: http://localhost:%s' % port)
    http_server.serve_forever()


if __name__ == "__main__":
    start()
