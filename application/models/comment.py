# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:36
# @filename: comment.py
from application import db


class Comment(db.Model):
    __tablename__ = 'blog_comment'
    user_id = db.Column(db.BIGINT(20), nullable=False, foreign_keys=db.ForeignKey('blog_user.id'))
    article_id = db.Column(db.BIGINT(20), nullable=False, foreign_keys=db.ForeignKey('blog_article.id'))
    pid = db.Column(db.BIGINT(20), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_publish = db.Column(db.TIMESTAMP, nullable=False)