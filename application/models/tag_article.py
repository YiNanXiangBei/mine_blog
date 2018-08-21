# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-19 下午1:30
# @filename: tag_article.py
from sqlalchemy.exc import SQLAlchemyError

from application import db, app


# from application.models.article import Article
# from application.models.tag import Tag


class TagArticle(db.Model):
    __tablename__ = 'blog_tag_article'
    tag_id = db.Column(db.BigInteger, db.ForeignKey('blog_tag.id'), primary_key=True)
    article_id = db.Column(db.BigInteger, db.ForeignKey('blog_article.id'), primary_key=True)

    def __init__(self, tag_id, article_id):
        self.tag_id = tag_id
        self.article_id = article_id

    def __str__(self):
        return "<TagArticle={}, {}>".format(self.tag_id, self.article_id)

    @staticmethod
    def save(tag_article):
        app.logger.info("save tag_article ...")
        db.session.add(tag_article)

    @staticmethod
    def delete(article_id):
        app.logger.info("delete tag_article ...")
        db.session.query(TagArticle).filter_by(article_id=article_id).delete()

    @staticmethod
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

    @staticmethod
    def flush():
        """
        提交刷新
        :return:
        """
        try:
            app.logger.info("commit session ....")
            db.session.flush()
        except SQLAlchemyError as e:
            app.logger.warning("commit session error: {}".format(e))
            db.session.rollback()
            reason = str(e)
            return reason
