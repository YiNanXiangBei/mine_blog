# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:36
# @filename: user.py
from application import db

uc = db.Table('uc',
              db.Column('uid', db.BIGINT(20), db.ForeignKey('blog_user.id')),
              db.Column('cid', db.BIGINT(20), db.ForeignKey('blog_comment.id'))
              )


class User(db.Model):
    __tablename__ = 'blog_user'
    id = db.Column(db.BIGINT(20), primary_key=True, unique=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    link = db.Column(db.String(50))
    avatar = db.Column(db.String(45))
    # 在Comment类中添加了一个属性为user，类型为User
    comments = db.relationship('Comment',
                               secondary=uc,
                               backref=db.backref('user', lazy='dynamic'),
                               lazy='dynamic')
