# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-2 下午2:46
# @filename: client_controller.py
from flask import Blueprint, request, jsonify

from application.auth.decrypt import decrypt
from application.constant import response
from application.constant.constant import Code, Message
from application.models.article import Article

client = Blueprint('/', __name__)


@client.route('/index', methods=['GET'])
@decrypt
def index(message):
    return jsonify(message)


@client.route('/detail_article', methods=['GET'])
@decrypt
def detail_article(message):
    """
    文章详细页面数据
    :param message:
    :return:
    """
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    article_id = message['data']['article_id']
    article = Article.get_by_id(article_id)
    if article:
        tags = []
        for tag in article.tags.all():
            sin_tag = {
                "id": tag.id,
                "tag": tag.tag
            }
            tags.append(sin_tag)
        previous = Article.get_previous(article.date_publish)
        next = Article.get_next(article.date_publish)
        result = {
            "id": article.id,
            "title": article.title,
            "desc": article.desc,
            "content": article.content,
            "publish_time": 'Posted by yinan on' + article.date_publish.strftime('%b %d,%Y'),
            "back_url": article.back_img,
            "tags": tags,
            "previous": previous[0] if previous else None,
            "next": next[0] if next else None
        }
        return jsonify(response.return_message(
            data={
                "article": result,
            },
            msg=Message.SUCCESS.value,
            code=Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        data=None,
        msg=Message.BAD_REQUEST.value,
        code=Code.BAD_REQUEST.value
    ))
