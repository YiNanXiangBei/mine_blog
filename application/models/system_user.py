# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: system_user.py
from application import db


class SysUser(db.Model):
    __tablename__ = 'system_user'
    id = db.Column(db.BIGINT(20), primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    avatar = db.Column(db.String(50))
    last_login = db.Column(db.TIMESTAMP)
