# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午9:37
# @filename: constant.py
"""
常量存储位置
"""
from enum import Enum, unique


@unique
class Constant(Enum):
    DELETED = '1'
    UN_DELETED = '0'


@unique
class Message(Enum):
    TOKEN_EXPIRED = 'Token过期，请重新登录'
    TOKEN_INVALID = 'Token无效，请重新登录'
    LOGIN_SUCCESS = '登录成功'
    LOGIN_FAILED = '登录失败'
    FORBIDDEN = '没有权限'
    BAD_REQUEST = '请求失败'
    SUCCESS = '请求成功'
    NOT_FOUND = '没有找到指定资源'
    NOT_FOUND_USER = '没有找到用户'


@unique
class Code(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    CREATED = 201
    NOT_CONTENT = 204
    NOT_FOUND = 404
    FORBIDDEN = 403
    REDIRECT = 301
