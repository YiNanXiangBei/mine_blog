# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-4 下午5:38
# @filename: sys_authenticate.py
import base64
import json
from functools import wraps

from flask import request
from application import app
from application.auth.sys_verificate import Verificate
from application.constant import response
from application.constant.constant import Code, Message
from application.models.system_user import SysUser


def jwt_required(func):
    """
    用户鉴权
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper():
        auth_token = request.headers.get('Authorization')
        if auth_token:
            auth_token_arr = auth_token.split(".")
            if not auth_token_arr or len(auth_token_arr) == 3:
                auth_header = json.loads(base64.b64decode(str(auth_token_arr[0]).encode()).decode())
                if auth_header['typ'] != 'JWT':
                    app.logger.warning("Please pass the correct verification header information")
                    result = response.return_message('', Message.TOKEN_INVALID.value, Code.BAD_REQUEST.value)
                else:
                    payload = Verificate.decode_auth_token(auth_token)
                    if not isinstance(payload, str):
                        users = SysUser.get_info_by_id(payload['data']['id'])
                        if users is None:
                            result = response.return_message('', Message.NOT_FOUND_USER.value, Code.BAD_REQUEST.value)
                        else:
                            if users.last_login == payload['data']['login_time']:
                                return_user = {
                                    'id': users.id,
                                    'username': users.username
                                }
                                app.logger.info("request success!")
                                result = response.return_message(return_user, Message.SUCCESS.value, Code.SUCCESS.value)
                            else:
                                app.logger.waring("Token hash been changed, please login again")
                                result = response.return_message('', Message.TOKEN_INVALID.value, Code.BAD_REQUEST.value)
                    else:
                        app.logger.info("login success redirect")
                        result = response.return_message('', payload, Code.REDIRECT.value)
            else:
                app.logger.warning("Please pass the correct verification header information")
                result = response.return_message('', Message.TOKEN_INVALID.value, Code.BAD_REQUEST.value)
        else:
            app.logger.warning("No certification Token is provided")
            result = response.return_message('', Message.TOKEN_INVALID.value, Code.BAD_REQUEST.value)
        return func(result)

    return wrapper
