# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-15 下午3:02
# @filename: sys_admin_controller.py
import json

from flask import Blueprint, render_template, request, jsonify

from application.auth.sys_authenticate import jwt_required
from application.auth.sys_verificate import set_password, Verificate
from application.constant import response
from application.constant.constant import Code, Message
from application.constant.util import CommonUtil
from application.models.system_user import SysUser

admin = Blueprint('sysadmin', __name__)


@admin.route("/validate_token", methods=['POST'])
@jwt_required
def validate(message):
    """
    校验token是否合法
    :return:
    """
    result = jsonify(message)

    return result


# @jwt_required
# @admin.route('/', methods=['GET'])
# def index():
#     return render_template('index.html')


# @admin.route('/login', methods=['GET'])
# def login_page():
#     '''
#     登录页面
#     :return:
#     '''
#     pass
#
#
# @jwt_required
# @admin.route('/upload', methods=['GET'])
# def upload_page():
#     '''
#     上传图片页面
#     :return:
#     '''
#     pass
#
#
@admin.route('/info', methods=['GET'])
@jwt_required
def info_page(message):
    """
    用户信息页面
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    username = request.values.get('username')
    sys_user = SysUser.get_info(username)
    token = Verificate.encode_auth_token(sys_user.id, sys_user.last_login.strftime("%Y-%m-%d %H:%M:%S"))
    data = {
        'info': {
            'username': sys_user.username,
            'password': sys_user.password,
            'email': sys_user.email,
            'avatar': sys_user.avatar
        },
        'token': token.decode()
    }
    return jsonify(response.return_message(data, Message.SUCCESS.value, Code.SUCCESS.value))


#
#
# @jwt_required
# @admin.route('/publish', methods=['GET'])
# def publish_page():
#     '''
#     发布文章页面
#     :return:
#     '''
#     pass
#
#
# @jwt_required
# @admin.route('/tags', methods=['GET'])
# def tag_page():
#     '''
#     显示标签页面
#     :return:
#     '''
#     pass
#
#
# @jwt_required
# @admin.route('/editor', methods=['GET'])
# def edit_page():
#     '''
#     编辑文章页面
#     :return:
#     '''
#     pass
#
#
@admin.route('/login', methods=['POST'])
def login():
    """
    管理员登录
    :return: 基本信息以及token
    """
    username = request.values.get('username')
    password = request.values.get('password')
    return Verificate.authenticate(username, password)


@admin.route('/register', methods=['POST'])
def register():
    """
    注册管理员
    :return: 用户基本信息
    """
    username = request.values.get('username')
    password = set_password(request.values.get('password'))
    email = request.values.get('email')
    avatar = request.values.get('avatar')
    sys_user = SysUser(username, password, email, avatar)
    result = SysUser.save(sys_user)
    if result is None:
        sys_user = SysUser.get_info(username)
        data = {
            "id": sys_user.id,
            "username": username
        }
        return jsonify(response.return_message(data, Message.REGISTER_SUCCESS.value, Code.SUCCESS.value))
    else:
        return jsonify(response.return_message(None, Message.REGISTER_FAILED.value, Code.BAD_REQUEST.value))


@admin.route('/upload', methods=['POST'])
@jwt_required
def upload(message):
    """
    上传图片
    :return: 返回图片链接
    """
    base64_str = request.values.get('img')
    CommonUtil.handle_img(base64_str, 'avatar.webp')
    return jsonify(message)
#
#
# @jwt_required
# @admin.route('/info', methods=['POST'])
# def change_info():
#     '''
#     修改个人信息
#     :return:
#     '''
#     pass
#
#
# @jwt_required
# @admin.route('/publish', methods=['POST'])
# def publish():
#     '''
#     发布文章
#     :return:
#     '''
#     pass
#
#
# @jwt_required
# @admin.route('/editor', methods=['POST'])
# def edit():
#     '''
#     编辑文章
#     :return:
#     '''
#     pass
#
#
# @jwt_required
# @admin.route('/add_tags', methods=['POST'])
# def addtag():
#     '''
#     添加标签
#     :return:
#     '''
#     pass
