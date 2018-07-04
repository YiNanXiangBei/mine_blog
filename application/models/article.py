# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: article.py
import datetime

from sqlalchemy.exc import SQLAlchemyError

from application import db
from application.constant.constant import Constant


class Article(db.Model):
    __tablename__ = 'blog_article'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    desc = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.TEXT, nullable=False)
    click_count = db.Column(db.BigInteger, nullable=False, default=0)
    date_publish = db.Column(db.TIMESTAMP, nullable=False)
    deleted = db.Column(db.String(1), nullable=False, default='0')
    # 在Comment中添加一个属性为article
    comments = db.relationship('Comment', backref='article')

    def __init__(self, title, desc, content, date_publish):
        self.title = title
        self.desc = desc
        self.content = content
        self.date_publish = date_publish

    def __str__(self):
        return '<Article{}, {}, {}, {}, {}>'. \
            format(self.id, self.title, self.desc,
                   self.click_count, self.date_publish)

    @staticmethod
    def get_all(page_no, page_size=10):
        articles = db.session.query(Article).filter_by(deleted=Constant.UN_DELETED.value).\
            paginate(page_no, page_size, False)
        return articles

    @staticmethod
    def get_by_id(article_id):
        article = db.session.query(Article).filter_by(id=article_id, deleted=Constant.UN_DELETED.value).first()
        return article

    @staticmethod
    def insert(article):
        db.session.add(article)
        session_commit()

    @staticmethod
    def delete(article_id):
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        db.session.query(Article).filter_by(id=article_id). \
            update({'deleted': Constant.DELETED.value, 'date_publish': now})
        session_commit()

    @staticmethod
    def update(article):
        db.session.query(Article).filter_by(id=article.id). \
            update({'title': article.title, 'desc': article.desc, 'content': article.content,
                    'date_publish': article.date_publish})


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason


if __name__ == '__main__':
    # now = datetime.datetime.now()
    # now = now.strftime("%Y-%m-%d %H:%M:%S")
    # article = Article('title', 'desc', 'content', now)
    Article.delete(3)
    result = Article.get_all(1)
    print(result.items)
