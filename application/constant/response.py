# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-4 下午5:52
# @filename: response.py


def return_message(data, msg, code):
    return {
        "code": code,
        "data": data,
        "msg": msg
    }
