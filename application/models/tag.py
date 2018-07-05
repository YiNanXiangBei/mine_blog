# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:36
# @filename: tag.py
from sqlalchemy.exc import SQLAlchemyError

from application import db, app

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

    def __init__(self, tag, articles=None):
        self.tag = tag
        self.articles = articles

    def __str__(self):
        return "<tag={}>".format(self.tag)

    @staticmethod
    def save(tags):
        """
        保存标签
        :param tags:
        :return:
        """
        app.logger.info("add tag ....")
        db.session.add(tags)
        session_commit()

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
