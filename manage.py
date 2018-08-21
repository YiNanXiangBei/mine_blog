from logging.config import dictConfig

from flask_cors import CORS

from application import app, configs
from application.controllers.client_controller import client

from application.controllers.sys_admin_controller import admin

CORS(admin)
CORS(client)
app.register_blueprint(client, url_prefix='/')
app.register_blueprint(admin, url_prefix='/sysadmin')

if __name__ == '__main__':
    dictConfig(configs.LOGGING_CONFIG)
    app.run()
