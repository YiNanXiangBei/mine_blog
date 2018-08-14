# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-15 下午3:02
# @filename: sys_admin_controller.py
import base64
import re
import time
import datetime

from flask import Blueprint, request, jsonify

from application.auth.sys_authenticate import jwt_required
from application.auth.sys_verificate import set_password, Verificate
from application.constant import response
from application.constant.constant import Code, Message, Constant
from application.constant.util import CommonUtil
from application.models.article import Article
from application.models.system_user import SysUser
from application.models.tag import Tag

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
    CommonUtil.handle_img(base64_str, 'avatar')
    remote_name = str(int(time.time()))
    CommonUtil.upload_img('avatar.jpg', remote_name, '.jpg')
    result = CommonUtil.upload_img('avatar.webp', remote_name)
    if result is not None:
        result_avatar = SysUser.update_avatar(username, result)
        if result_avatar is None:
            return jsonify(response.return_message(
                data={
                    'image_url': result,
                    'token': Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
                },
                msg=Message.UPLOAD_SUCCESS.value,
                code=Code.SUCCESS.value
            ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.UPLOAD_FAILED.value,
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
    img = CommonUtil.handle_img(base64_str, 'files')
    remote_name = str(int(time.time()))
    CommonUtil.upload_img('files.jpg', remote_name, '.jpg')
    result = CommonUtil.upload_img('files.webp', remote_name)
    if request.values.get('back_img'):
        remote_name = remote_name + '.tiny'
        CommonUtil.tiny_img_thumb(img, 'tiny_files')
        CommonUtil.upload_img('tiny_files.jpg', remote_name, '.jpg')
        CommonUtil.upload_img('tiny_files.webp', remote_name)
    if result is not None:
        return jsonify(response.return_message(
            data={
                'image_url': result,
                'token': Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.UPLOAD_SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.UPLOAD_FAILED,
        code=Code.BAD_REQUEST.value
    ))


@admin.route('/article', methods=['POST'])
@jwt_required
def post_publish(message):
    """
    发布文章
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    results = request.values.to_dict()
    if Article.get_id_by_title(results['title']) is not None:
        return jsonify(response.return_message(
            data={
                "token": Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.TITLE_EXISTS.value,
            code=Code.TITLE_EXISTS.value
        ))
    article = Article(results['title'], results['desc'], results['content'], datetime.datetime.now().
                      strftime("%Y-%m-%d %H:%M:%S"), results['back_img'])
    # 将前台传来的字符串，转换成列表，再转换成元组,然后通过标签查询id
    tag_ids = Tag.get_id_by_tag(tuple(eval(results['tags'])))
    result = Article.insert(article, tag_ids)
    if result is None:
        return jsonify(response.return_message(
            data={
                "token": Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.BAD_REQUEST.value,
        code=Code.BAD_REQUEST.value
    ))


@admin.route('/article', methods=['DELETE'])
@jwt_required
def delete_publish(message):
    """
    删除文章
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    article_id = request.values.get('article_id')
    result = Article.delete(article_id)
    if result is None:
        return jsonify(response.return_message(
            data={
                'token': Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.DELETE_SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.DELETE_FAILED.value,
        code=Code.BAD_REQUEST.value
    ))


@admin.route('/article', methods=['PUT'])
@jwt_required
def put_publish(message):
    """
    修改文章
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    results = request.values.to_dict()
    if Article.get_by_id(results['article_id']) is None:
        return jsonify(response.return_message(
            data={
                "token": Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.ARTICLE_NOT_EXISTS.value,
            code=Code.NOT_FOUND.value
        ))
    article = Article(results['title'], results['desc'], results['content'], datetime.datetime.now().
                      strftime("%Y-%m-%d %H:%M:%S"), results['back_img'])
    article.id = results['article_id']
    # 将前台传来的字符串，转换成列表，再转换成元组,然后通过标签查询id
    tag_ids = Tag.get_id_by_tag(tuple(eval(results['tags'])))

    if Article.update(article, tag_ids) is None:
        return jsonify(response.return_message(
            data={
                "token": Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.BAD_REQUEST.value,
        code=Code.BAD_REQUEST.value
    ))


@admin.route('/article', methods=['GET'])
@jwt_required
def get_publish(message):
    """
    查询文章
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    article_id = request.values.get("article_id")
    article = Article.get_by_id(article_id)
    if article:
        tags = [tag.tag for tag in article.tags.all()]
        result = {
            "id": article.id,
            "title": article.title,
            "tags": tags,
            "desc": article.desc,
            "content": article.content,
            'back_img': article.back_img
        }
        return jsonify(response.return_message(
            data={
                "article": result,
                "token": Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.BAD_REQUEST.value,
        code=Code.BAD_REQUEST.value
    ))


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

@admin.route('/tags', methods=['GET'])
@jwt_required
def gettags(message):
    """
    获取标签
    :param message:
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    tags = Tag.get_all()
    tags_value = [tag.tag for tag in tags]
    return jsonify(response.return_message(
        data={
            'tags': tags_value,
            'token': Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
        },
        msg=Message.SUCCESS.value,
        code=Code.SUCCESS.value
    ))


@admin.route('/add_tags', methods=['POST'])
@jwt_required
def addtag(message):
    """
    添加标签
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    new_tag = request.values.get('tag')
    tag = Tag(new_tag)
    result = Tag.save(tag)
    if result is None:
        return jsonify(response.return_message(
            data={
                'token': Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
            },
            msg=Message.SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.BAD_REQUEST.value,
        code=Code.BAD_REQUEST.value
    ))


@admin.route('/blurry_tags', methods=['GET'])
@jwt_required
def get_by_tag(message):
    """
    模糊查询tag
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    tag_value = request.values.get('tag')
    tags = Tag.get_by_tag(tag_value)
    tags_value = [tag.tag for tag in tags]
    return jsonify(response.return_message(
        data={
            'tags': tags_value,
            'token': Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode()
        },
        msg=Message.SUCCESS.value,
        code=Code.SUCCESS.value
    ))


@admin.route('/oldArticles', methods=['GET'])
@jwt_required
def get_editor_article(message):
    """
    分页查询
    :param message:
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    params = request.values.to_dict()
    start_time = params['beginTime']
    end_time = params['endTime']
    page_no = params['pageNo']
    result = Article.get_all_by_date(start_time, end_time, page_no)
    articles = []
    for item in result.items:
        tags = [tag.tag for tag in item.tags.all()]
        article = {
            "id": item.id,
            "title": item.title,
            "tags": tags,
            "datetime": item.date_publish.strftime("%Y-%m-%d")
        }
        articles.append(article)
    return jsonify(response.return_message(
        data={
            "articles": articles,
            "token": Verificate.encode_auth_token(message['data']['id'], message['data']['last_login']).decode(),
            "total": result.total
        },
        msg=Message.SUCCESS.value,
        code=Code.SUCCESS.value
    ))


@admin.route('/verify', methods=['POST'])
def verify():
    """
    校验用户名和邮箱
    :return:
    """
    params = request.values.to_dict()
    enter_username = params['username']
    enter_email = params['email']
    # 用户信息校验成功
    if SysUser.verify(enter_username, enter_email) is True:
        # 获取毫秒级时间戳
        t = time.time()
        ms_t = int(round(t * 1000))
        # 将邮箱前两位设为*
        '''
            re.sub()有5个参数，三个必选参数pattern,repl,string；两个可选参数count,flags
            re.sub(pattern,repl,string,count,flags)
            pattern:表示正则表达式中的模式字符串；
            repl:被替换的字符串，或者是一个方法（既可以是字符串，也可以是函数）；
            当repl为字符串的时候，也就是需要 将string中与pattern匹配的字符串都替换成repl
            当repl为方法的时候，就必须是一个带有一个参数，且参数为MatchObject类型的方法，该方法需要返回一个字符串。 
            string:要被处理的，要被替换的字符串；
            count:指的是最大的可以被替换的匹配到的字符串的个数，默认为0，就是所有匹配到的字符串。 
            flgas:标志位
         '''
        reset_email1 = re.sub(enter_email[:2], '**', enter_email)

        # 整合参数格式
        encrypt_params = 'username={}&email={}&timestamp={}'.format(enter_username, reset_email1, str(ms_t))
        # .encode() ：用来转换成bytes数组
        sid = base64.b64encode(encrypt_params.encode()).decode()
        # 接收发送返回消息
        send_result = CommonUtil.send_email(enter_email, sid)
        # 如果发送失败，则会返回失败原因
        if send_result:
            return jsonify(response.return_message(
                data=send_result,
                msg=Message.EMAIL_SEND_FAILED.value,
                code=Code.FORBIDDEN.value
            ))
        # 否则发送成功
        return jsonify(response.return_message(
            data=None,
            msg=Message.EMAIL_SEND_SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    # 用户信息校验失败
    else:
        return jsonify(response.return_message(
            data=None,
            msg=Message.VERIFY_FAILED.value,
            code=Code.BAD_REQUEST.value
        ))


@admin.route('/resetPwd', methods=['PUT'])
def reset_pwd():
    """
    重置密码
    :return:
    """
    params = request.values.to_dict()
    password = params['password']
    if password is None or len(password) < Constant.PASSWORD_LENGTH.value:
        return jsonify(response.return_message(None, Message.PASSWORD_LENGTH_LESS_THAN.value, Code.BAD_REQUEST.value))
    passwords = set_password(password)
    result = SysUser.reset_password(params['username'], passwords)
    if result is None:
        return jsonify(response.return_message(None, Message.SUCCESS.value, Code.SUCCESS.value))
    else:
        return jsonify(response.return_message(None, Message.RESET_PASSWORD_FAILED.value, Code.BAD_REQUEST.value))
