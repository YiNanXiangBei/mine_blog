# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: article.py
from application import db


class Article(db.Model):
    __tablename__ = 'blog_article'
    id = db.Column(db.BIGINT(20), primary_key=True, nullable=False, unique=True)
    tag_id = db.Column(db.BIGINT(20), nullable=False)
    title = db.Column(db.String(50), nullable=False, unique=True)
    desc = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.TEXT, nullable=False)
    click_count = db.Column(db.BIGINT(20), nullable=False, default=0)
    date_publish = db.Column(db.TIMESTAMP, nullable=False)
    # 在Comment中添加一个属性为article
    comments = db.relationship('Comment', backref='article')
