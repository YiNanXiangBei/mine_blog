# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-24 下午1:10
# @filename: web.py.py
from logging.config import dictConfig

from flask_cors import CORS
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from application import app, configs
from application.controllers.client_controller import client
from application.controllers.sys_admin_controller import admin

CORS(admin)
CORS(client)
app.register_blueprint(client, url_prefix='/')
app.register_blueprint(admin, url_prefix='/sysadmin')
dictConfig(configs.LOGGING_CONFIG)

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.current().start()
