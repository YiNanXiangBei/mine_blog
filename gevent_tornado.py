# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-28 下午2:53
# @filename: gevent_tornado.py.py
import gevent.pywsgi
from gevent import monkey
from logging.config import dictConfig
from flask_cors import CORS
from application import app, configs
from application.controllers.client_controller import client
from application.controllers.sys_admin_controller import admin

CORS(admin)
CORS(client)
app.register_blueprint(client, url_prefix='/')
app.register_blueprint(admin, url_prefix='/sysadmin')
dictConfig(configs.LOGGING_CONFIG)
monkey.patch_all()

if __name__ == "__main__":
    server = gevent.pywsgi.WSGIServer(('', 5000), app)
    server.serve_forever()