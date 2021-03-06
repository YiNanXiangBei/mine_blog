# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:36
# @filename: user.py
from sqlalchemy.exc import SQLAlchemyError

from application import db, app

uc = db.Table('uc',
              db.Column('uid', db.BIGINT(20), db.ForeignKey('blog_user.id')),
              db.Column('cid', db.BIGINT(20), db.ForeignKey('blog_comment.id'))
              )


class User(db.Model):
    __tablename__ = 'blog_user'
    id = db.Column(db.BIGINT(20), primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(45), unique=True, nullable=False)
    link = db.Column(db.String(200))
    avatar = db.Column(db.String(200))
    # 在Comment类中添加了一个属性为user，类型为User
    comments = db.relationship('Comment',
                               secondary=uc,
                               backref=db.backref('user', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, id, username, link, avatar, comments=None):
        self.id = id
        self.username = username
        self.link = link
        self.avatar = avatar
        self.comments = comments

    def __str__(self):
        return "<username={}, link={}, avatar={}>".format(self.username, self.link, self.avatar)

    @staticmethod
    def get_info_by_id(user_id):
        """
        依据id查询用户
        :param user_id:
        :return:
        """
        app.logger.info("get info by id ....")
        return db.session.query(User).filter(id=user_id).first()

    @staticmethod
    def save(user):
        """
        保存用户
        :param user:
        :return:
        """
        app.logger.info("add user ....")
        db.session.add(user)
        session_commit()

    @staticmethod
    def get_info(username):
        """
        依据用户名查询用户
        :param username:
        :return:
        """
        app.logger.info("get user info ....")
        return db.session.query(User).filter(username=username).first()


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
