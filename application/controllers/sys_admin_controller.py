# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-15 下午3:02
# @filename: sys_admin_controller.py
import base64

from flask import Blueprint, request, jsonify

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
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    base64_str = request.values.get('img')
    username = request.values.get('username')
    CommonUtil.handle_img(base64_str, 'avatar.webp')
    result = CommonUtil.upload_img('avatar.webp')
    if result is not None:
        result_avatar = SysUser.update_avatar(username, result)
        if result_avatar is None:
            return jsonify(response.return_message(
                data={
                    'image_url': result
                },
                msg=Message.UPLOAD_SUCCESS.value,
                code=Code.SUCCESS.value
            ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.UPLOAD_FAILED,
        code=Code.BAD_REQUEST.value
    ))


@admin.route('/info', methods=['POST'])
@jwt_required
def change_info(message):
    """
    修改个人信息
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    params = request.values.to_dict()
    passwords = set_password(params['password'])
    sys_user = SysUser(params['username'], passwords, params['email'], params['avatar'])
    result = SysUser.update(sys_user)
    if result is None:
        # 为空说明存入数据库没有报错
        sys_user = SysUser.get_info(params['username'])
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
    else:
        return jsonify(response.return_message(None, Message.BAD_REQUEST.value, Code.BAD_REQUEST.value))


@admin.route('/upload_image', methods=['POST'])
@jwt_required
def upload_image(message):
    """
    图片上传到腾讯cos
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    base64_str = base64.b64encode(request.files['file'].read()).decode('utf-8')
    filename = "files.webp"
    CommonUtil.handle_img(base64_str, filename)
    result = CommonUtil.upload_img(filename)
    if result is not None:
        return jsonify(response.return_message(
            data={
                'image_url': result
            },
            msg=Message.UPLOAD_SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.UPLOAD_FAILED,
        code=Code.BAD_REQUEST.value
    ))

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
