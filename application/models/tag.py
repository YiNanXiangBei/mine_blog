# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:36
# @filename: tag.py
from sqlalchemy.exc import SQLAlchemyError

from application import db, app
from application.models.article import Article
from application.models.tag_article import TagArticle


class Tag(db.Model):
    __tablename__ = 'blog_tag'
    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False, autoincrement=True)
    tag = db.Column(db.String(20), nullable=False, unique=True)
    # 在Article 中添加一个属性为tags,同时在Tag类中添加属性为articles
    articles = db.relationship('Article', secondary="blog_tag_article",
                               backref=db.backref('tags', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return "<tag={}>".format(self.tag)

    @staticmethod
    def save(tag):
        """
        保存标签
        :param tag:
        :return:
        """
        app.logger.info("add tag ....")
        db.session.add(tag)
        return session_commit()

    @staticmethod
    def get_all():
        """
        查询所有标签
        :return:
        """
        return db.session.query(Tag).all()

    @staticmethod
    def get_by_tag(tag):
        """
        模糊查询所有满足条件的标签
        :param tag:
        :return:
        """
        app.logger.info("get tag ....")
        value = '{}%'.format(tag)
        return db.session.query(Tag).filter(Tag.tag.like(value)).all()


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
