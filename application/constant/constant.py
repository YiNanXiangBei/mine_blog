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
    TWO = 2
    PASSWORD_LENGTH = 6
    WEBP_IMG = 'image/webp'


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
    CAN_NOT_GENERATE_TOKEN = '无法生成Token，请联系管理员'
    REGISTER_FAILED = '注册失败'
    REGISTER_SUCCESS = '注册成功'
    UPLOAD_SUCCESS = '上传成功'
    UPLOAD_FAILED = '上传失败'
    TITLE_EXISTS = '文章标题已经存在'
    ARTICLE_NOT_EXISTS = '文章不存在'
    DELETE_SUCCESS = '删除成功'
    DELETE_FAILED = '删除失败'
    VERIFY_SUCCEED = '用户信息验证成功'
    VERIFY_FAILED = '用户信息验证失败'
    EMAIL_SEND_FAILED = '邮件发送失败'
    EMAIL_SEND_SUCCESS = '邮件发送成功'
    PASSWORD_LENGTH_LESS_THAN = '密码长度小于6位'
    RESET_PASSWORD_FAILED = "重置密码失败，请确认该用户是否存在，或联系管理员！"


@unique
class Code(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    CREATED = 201
    NOT_CONTENT = 204
    NOT_FOUND = 404
    FORBIDDEN = 403
    REDIRECT = 301
    UNAUTHORIZED = 401
    TITLE_EXISTS = 417
