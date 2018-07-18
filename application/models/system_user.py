# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: system_user.py
from sqlalchemy.exc import SQLAlchemyError

from application import db, app


class SysUser(db.Model):
    __tablename__ = 'system_user'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    avatar = db.Column(db.String(100))
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
        app.logger.info("add sys_user ....")
        db.session.add(sys_user)
        return session_commit()

    @staticmethod
    def get_info(username):
        """
        查询密码（不提供给前端，仅用于校验）
        :param username:
        :return:
        """
        app.logger.info("get info by username ....")
        user_info = db.session.query(SysUser).filter_by(username=username).first()
        return user_info

    @staticmethod
    def get_info_by_id(id):
        """
        依据id查询用户信息
        :param id:
        :return:
        """
        app.logger.info("get info by id ....")
        user_info = db.session.query(SysUser).filter_by(id=id).first()
        return user_info

    @staticmethod
    def update(sys_user):
        """
        更新用户数据
        :param sys_user:
        :return:
        """
        app.logger.info("update sys_user ....")
        db.session.query(SysUser).filter_by(username=sys_user.username). \
            update({'password': sys_user.password, 'email': sys_user.email})
        return session_commit()

    @staticmethod
    def update_login_time(user_id, login_time):
        """
        修改上次登录时间
        :param user_id:
        :param login_time:
        :return:
        """
        app.logger.info("update user_id, login_time ....")
        db.session.query(SysUser).filter_by(id=user_id). \
            update({'last_login': login_time})
        return session_commit()

    @staticmethod
    def update_avatar(username, avatar):
        """
        更新头像
        :param avatar:
        :param username:
        :return:
        """
        app.logger.info('update sys_user avatar ...')
        db.session.query(SysUser).filter_by(username=username). \
            update({'avatar': avatar})
        return session_commit()


def session_commit():
    """
    事务提交，如果失败则回滚
    :return:
    """
    try:
        app.logger.info("commit session ....")
        db.session.commit()
    except SQLAlchemyError as e:
        app.logger.warning("commit session error: {}".format(e))
        db.session.rollback()
        reason = str(e)
        return reason
