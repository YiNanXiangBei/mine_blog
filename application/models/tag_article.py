# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-19 下午1:30
# @filename: tag_article.py
from application import db
# from application.models.article import Article
# from application.models.tag import Tag


class TagArticle(db.Model):
    __tablename__ = 'blog_tag_article'
    tag_id = db.Column(db.BigInteger, db.ForeignKey('blog_tag.id'), primary_key=True)
    article_id = db.Column(db.BigInteger, db.ForeignKey('blog_article.id'), primary_key=True)
