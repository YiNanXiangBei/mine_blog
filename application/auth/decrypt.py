# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-3 下午3:43
# @filename: encrypt.py
from functools import wraps

from flask import request

from application import app
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
        result = CommonUtil.decrypt(params)
        if result is None:
            return_result = response.return_message(None, Message.BAD_REQUEST.value, Code.BAD_REQUEST.value)
        else:
            return_result = response.return_message(result, Message.SUCCESS.value, Code.SUCCESS.value)
        return func(return_result)

    return wrapper
