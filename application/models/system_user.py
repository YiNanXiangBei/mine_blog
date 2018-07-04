# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: system_user.py
from sqlalchemy.exc import SQLAlchemyError

from application import db


class SysUser(db.Model):
    __tablename__ = 'system_user'
    id = db.Column(db.BIGINT(20), primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    avatar = db.Column(db.String(50))
    last_login = db.Column(db.TIMESTAMP)

    def __init__(self, username, password, email, avatar=None):
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar

    def __str__(self):
        return "<username={}, email={}, avatar={}>".format(self.username, self.email, self.avatar)

    @staticmethod
    def save(sys_user):
        """
        新增系统用户
        :param sys_user:
        :return:
        """
        db.session.add(sys_user)
        session_commit()

    @staticmethod
    def get_info(username):
        """
        查询密码（不提供给前端，仅用于校验）
        :param username:
        :return:
        """
        user_info = db.session.query(SysUser).filter_by(username=username).first()
        return user_info

    @staticmethod
    def update(sys_user):
        """
        更新用户数据
        :param sys_user:
        :return:
        """
        db.session.query(SysUser).filter_by(id=sys_user.id). \
            update({'password': sys_user.password, 'email': sys_user.email,
                    'avatar': sys_user.avatar, 'last_login': sys_user.last_login})
        session_commit()

    @staticmethod
    def update_login_time(user_id, login_time):
        """
        修改上次登录时间
        :param user_id:
        :param login_time:
        :return:
        """
        db.session.query(SysUser).filter_by(id=user_id). \
            update({'last_login': login_time})
        session_commit()


def session_commit():
    """
    事务提交，如果失败则回滚
    :return:
    """
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
