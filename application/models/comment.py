# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:36
# @filename: comment.py
import datetime

from sqlalchemy.exc import SQLAlchemyError

from application import db
from application.constant.constant import Constant


class Comment(db.Model):
    __tablename__ = 'blog_comment'
    comment_id = db.Column(db.BigInteger, nullable=False, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('blog_user.id'), nullable=False)
    article_id = db.Column(db.BigInteger, db.ForeignKey('blog_article.id'), nullable=False)
    pid = db.Column(db.BigInteger, nullable=False, default=0)
    content = db.Column(db.String(200), nullable=False)
    date_publish = db.Column(db.TIMESTAMP, nullable=False)
    deleted = db.Column(db.String(1), nullable=False, default='0')

    def __init__(self, user_id, article_id, content, pid=0):
        self.user_id = user_id
        self.article_id = article_id
        self.pid = pid
        self.content = content

    def __str__(self):
        return "<user_id={}, article_id={}, pid={}, content={}>". \
            format(self.user_id, self.article_id, self.pid, self.content)

    @staticmethod
    def insert(comment):
        """
        新增评论
        :param comment: 实体类
        :return:
        """
        db.session.add(comment)
        session_commit()

    @staticmethod
    def delete(comment_id):
        """
        删除评论
        :param comment_id:
        :return:
        """
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        db.session.query(Comment).filter_by(comment_id=comment_id). \
            update({'deleted': Constant.DELETED.value, 'date_publish': now})
        session_commit()

    @staticmethod
    def update(comment):
        """
        更新评论
        :param comment:
        :return:
        """
        db.session.query(Comment).filter_by(comment_id=comment.comment_id). \
            update({'content': comment.content,
                    'date_publish': comment.date_publish})
        session_commit()

    @staticmethod
    def get_all(page_no, page_size=10):
        """
        分页查询评论
        :param page_no:
        :param page_size:
        :return:
        """
        comments = db.session.query(Comment).filter_by(deleted=Constant.UN_DELETED.value). \
            paginate(page_no, page_size, False)
        return comments


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

