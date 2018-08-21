# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-3 下午3:43
# @filename: encrypt.py
from functools import wraps

from flask import request

from application import app
from application.configs import ENCRYPT_KEY
from application.constant import response
from application.constant.constant import Message, Code
from application.constant.util import CommonUtil


def decrypt(func):
    """
    数据解密
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper():
        app.logger.info("request ip: {}".format(request.remote_addr))
        params = request.values.get('params')
        app.logger.info("begin to rsa decrypt ...")
        result = CommonUtil.rsa_decrypt(ENCRYPT_KEY.get('private_key'), params)
        if result is None:
            return_result = response.return_message(None, Message.BAD_REQUEST.value, Code.BAD_REQUEST.value)
        else:
            result = eval(result)
            # 字符串类型的16位长度key,16进制字符串类型的data
            app.logger.info("begin to aes decrypt ...")
            params = CommonUtil.aes_decrypt(result.get('key'), result.get('data'))
            app.logger.info("decrypt request params: {}".format(params))
            return_result = response.return_message(eval(params), Message.SUCCESS.value, Code.SUCCESS.value)
        return func(return_result)

    return wrapper
