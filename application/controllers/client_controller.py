# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-2 下午2:46
# @filename: client_controller.py
from flask import Blueprint, request, jsonify, redirect

from application import configs
from application.auth.decrypt import decrypt
from application.constant import response
from application.constant.constant import Code, Message, Constant
from application.models.article import Article
from application.models.tag import Tag

client = Blueprint('/', __name__)


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
        Article.update_click_count(article_id)
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


@client.route('/tags', methods=['GET'])
def tags():
    """
    获取所有标签
    :return:
    """
    tags = Tag.get_all()
    if tags:
        data_tag = []
        for tag in tags:
            sin_tag = {
                "id": tag.id,
                "tag": tag.tag
            }
            data_tag.append(sin_tag)
        return jsonify(response.return_message(
            {
                'tags': data_tag
            },
            Message.SUCCESS.value,
            Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        None,
        Message.SUCCESS.value,
        Code.SUCCESS.value
    ))


@client.route('/tag_articles', methods=['GET'])
@decrypt
def get_tag_articles(message):
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    tag_id = message['data']['tag_id']
    page_no = message['data']['page_no']
    articles = Tag.get_tag_by_id(tag_id, page_no)
    article_list = []
    if articles:
        for item in articles.items:
            article_list.append({
                'id': item.id,
                'title': item.title,
                'desc': item.desc,
                'content': item.content,
                'publish_time': item.date_publish,
                'back_url': item.back_img.replace('.webp', '.tiny.webp') if item.back_img else None
            })
        return jsonify(response.return_message(
            {
                'total': articles.total,
                'articles': article_list
            },
            Message.SUCCESS.value,
            Code.SUCCESS.value
        ))
    return jsonify(response.return_message(None, Message.BAD_REQUEST.value, Code.BAD_REQUEST.value))


@client.route('/index', methods=['GET'])
@decrypt
def index(message):
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    page_num = message['data']['page']
    articles = Article.get_article_by_pageno(page_num)
    if articles:
        article_list = []
        for item in articles.items:
            article = {
                "id": item.id,
                "title": item.title,
                "desc": item.desc,
                "content": item.content,
                "publish_time": 'Posted by yinan on ' + item.date_publish.strftime('%b %d,%Y'),
            }
            article_list.append(article)
        top_articles = []
        for item in Article.get_top5():
            top_articles.append({
                'id': item.id,
                'title': item.title
            })
        return jsonify(response.return_message(
            {
                "total": articles.total,
                "articles": article_list,
                'top_articles': top_articles
            },
            Message.SUCCESS.value,
            Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        None,
        Message.BAD_REQUEST.value,
        Code.BAD_REQUEST.value
    ))


@client.route('/search', methods=['GET'])
@decrypt
def search(message):
    if message['code'] != Code.SUCCESS.value:
        return jsonify(message)
    input_search = message['data']['search_params']
    articles = Article.get_by_search(input_search)
    if articles:
        article_list = []
        for item in articles:
            article = {
                "id": item.id,
                "title": item.title,
                "content": item.content
            }
            article_list.append(article)
        return jsonify(response.return_message(
            {
                "articles": article_list
            },
            Message.SUCCESS.value,
            Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        None,
        Message.BAD_REQUEST.value,
        Code.BAD_REQUEST.value
    ))


@client.route('/archive', methods=['GET'])
def archive():
    articles = Article.get_by_archive()
    if articles:
        publish_years = Article.get_archive_year()
        archive_list = []
        for year in publish_years:
            article_list = []
            for article in articles:
                if year[0] == article[1]:
                    article_list.append({
                        "id": article[0].id,
                        "publish_time": article[0].date_publish.strftime('%b %d,%Y'),
                        "title": article[0].title
                    })
            archive_list.append({
                'publish_date': year[0],
                'articles': article_list
            })
        return jsonify(response.return_message(
            archive_list,
            Message.SUCCESS.value,
            Code.SUCCESS.value
        ))
    return jsonify(response.return_message(
        None,
        Message.BAD_REQUEST.value,
        Code.BAD_REQUEST.value
    ))


@client.route('/image/<image_id>', methods=['GET'])
def image(image_id):
    tencent_config = configs.TENCENT_OAUTH
    accept = request.headers.get('Accept')
    image_url = 'http://{}.cosgz.myqcloud.com/{}'.format(tencent_config.get('bucket'), image_id)
    if accept.find(Constant.WEBP_IMG.value) == -1:
        image_url = image_url.replace('webp', 'jpg')
    return redirect(image_url)
