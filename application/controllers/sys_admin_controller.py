# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-15 下午3:02
# @filename: sys_admin_controller.py
from flask import Blueprint

from application.auth.sys_authenticate import jwt_required

admin = Blueprint('sysadmin', __name__)


@admin.route('/login', methods=['GET'])
def login_page():
    '''
    登录页面
    :return:
    '''
    pass


@jwt_required
@admin.route('/upload', methods=['GET'])
def upload_page():
    '''
    上传图片页面
    :return:
    '''
    pass


@jwt_required
@admin.route('/info', methods=['GET'])
def info_page():
    '''
    用户信息页面
    :return:
    '''
    pass


@jwt_required
@admin.route('/publish', methods=['GET'])
def publish_page():
    '''
    发布文章页面
    :return:
    '''
    pass


@jwt_required
@admin.route('/tags', methods=['GET'])
def tag_page():
    '''
    显示标签页面
    :return:
    '''
    pass


@jwt_required
@admin.route('/editor', methods=['GET'])
def edit_page():
    '''
    编辑文章页面
    :return:
    '''
    pass


@admin.route('/login', methods=['POST'])
def login():
    '''
    管理员登录
    :return: 基本信息以及token
    '''
    pass


@jwt_required
@admin.route('/upload', methods=['POST'])
def upload():
    '''
    上传图片
    :return: 返回图片链接
    '''
    pass


@jwt_required
@admin.route('/info', methods=['POST'])
def change_info():
    '''
    修改个人信息
    :return:
    '''
    pass


@jwt_required
@admin.route('/publish', methods=['POST'])
def publish():
    '''
    发布文章
    :return:
    '''
    pass


@jwt_required
@admin.route('/editor', methods=['POST'])
def edit():
    '''
    编辑文章
    :return:
    '''
    pass


@jwt_required
@admin.route('/add_tags', methods=['POST'])
def addtag():
    '''
    添加标签
    :return:
    '''
    pass
