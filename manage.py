from flask_cors import CORS

from application import app
from application.controllers.client_controller import client

from application.controllers.sys_admin_controller import admin
CORS(admin)
app.register_blueprint(client, url_prefix='/')
app.register_blueprint(admin, url_prefix='/sysadmin')



if __name__ == '__main__':
    app.run()
