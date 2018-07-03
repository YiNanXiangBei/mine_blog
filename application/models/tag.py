# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:36
# @filename: tag.py
from application import db

at = db.Table('at',
              db.Column('article_id', db.BIGINT(20), db.ForeignKey('blog_article.id')),
              db.Column('tag_id', db.BIGINT(20), db.ForeignKey('blog_tag.id'))
              )


class Tag(db.Model):
    __tablename__ = 'blog_tag'
    id = db.Column(db.BIGINT(20), primary_key=True, unique=True, nullable=False, autoincrement=True)
    tag = db.Column(db.String(20), nullable=False, unique=True)
    articles = db.relationship('Article', secondary=at,
                               backref=db.backref('tags', lazy='dynamic'),
                               lazy='dynamic')
