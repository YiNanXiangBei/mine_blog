# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-4 下午5:37
# @filename: sys_verificate.py
import datetime
import jwt
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from application import configs, app
from application.constant import response
from application.constant.constant import Message, Code
from application.models.system_user import SysUser


class Verificate(object):
    """
    系统校验
    """

    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证token
        :param user_id:
        :param login_time:
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.now() + configs.JWT_EXPIRATION_DELTA,
                'iat': datetime.datetime.now(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                configs.JWT_SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            app.logger.error("Generate token failed: {}".format(e))

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证token
        :param auth_token:
        :return:
        """
        try:
            payload = jwt.decode(auth_token, configs.JWT_SECRET_KEY, options={'verify': False})
            if 'data' in payload and 'id' in payload['data']:
                app.logger.info("decode token success : {}".format(payload))
                return payload
            else:
                app.logger.error("invalid token error: {}".format(jwt.InvalidTokenError))
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            app.logger.warning("expired token: {}".format(auth_token))
            return Message.TOKEN_EXPIRED.value
        except jwt.InvalidTokenError:
            app.logger.warning("invalid token: {}".format(auth_token))
            return Message.TOKEN_INVALID.value

    @staticmethod
    def authenticate(username, password):
        """
        用户登录，登录成功返回token, 登录失败返回失败原因
        :param username:
        :param password:
        :return:
        """
        user_info = SysUser.get_info(username)
        if user_info is None:
            app.logger.warning("can not find user: {}".format(username))
            return jsonify(response.return_message('', Message.BAD_REQUEST.value, Code.BAD_REQUEST.value))
        else:
            if check_password(user_info.password, password):
                app.logger.debug("check password success ...")
                now = datetime.datetime.now()
                login_time = now.strftime("%Y-%m-%d %H:%M:%S")
                SysUser.update_login_time(user_info.id, login_time)
                token = Verificate.encode_auth_token(user_info.id, login_time)
                if token is None:
                    return jsonify(response.
                                   return_message('', Message.CAN_NOT_GENERATE_TOKEN.value, Code.BAD_REQUEST.value))
                else:
                    return jsonify(
                        response.return_message(token.decode(), Message.LOGIN_SUCCESS.value, Code.SUCCESS.value))
            else:
                app.logger.debug("check password error ...")
                return jsonify(response.return_message('', Message.LOGIN_FAILED.value, Code.BAD_REQUEST.value))


def check_password(hash, password):
    app.logger.info("check password hash ....")
    return check_password_hash(hash, password)


def set_password(password):
    app.logger.info("generate password hash ....")
    return generate_password_hash(password)
