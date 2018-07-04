# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-4 下午5:37
# @filename: sys_verificate.py
import datetime
import time
import jwt
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from application import configs
from application.constant import response
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
                'exp': datetime.datetime.utcnow() + configs.JWT_EXPIRATION_DELTA,
                'iat': datetime.datetime.utcnow(),
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
            return e

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
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token 过期请重新登录'
        except jwt.InvalidTokenError:
            return '无效 Token，请重新登录'

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token, 登录失败返回失败原因
        :param username:
        :param password:
        :return:
        """
        user_info = SysUser.get_info(username)
        if user_info is None:
            return jsonify(response.return_message('', '找不到用户', 400))
        else:
            if check_password(user_info.password, password):
                login_time = int(time.time())
                SysUser.update_login_time(user_info.id, login_time)
                token = self.encode_auth_token(user_info.id, login_time)
                return jsonify(response.return_message(token.decode(), '登录成功', 200))
            else:
                return jsonify(response.return_message('', '密码不正确', 400))


def check_password(hash, password):
    return check_password_hash(hash, password)


def set_password(password):
    return generate_password_hash(password)
