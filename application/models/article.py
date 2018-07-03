# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: article.py
import time
from sqlalchemy.exc import SQLAlchemyError

from application import db
from application.constant.constant import Constant


class Article(db.Model):
    __tablename__ = 'blog_article'
    id = db.Column(db.BIGINT(20), primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    desc = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.TEXT, nullable=False)
    click_count = db.Column(db.BIGINT(20), nullable=False, default=0)
    date_publish = db.Column(db.TIMESTAMP, nullable=False)
    deleted = db.Column(db.String(1), nullable=False, default='0')
    # 在Comment中添加一个属性为article
    comments = db.relationship('Comment', backref='article')

    def __init__(self, title, desc, content, click_count, date_publish, deleted):
        self.title = title
        self.desc = desc
        self.content = content
        self.click_count = click_count
        self.date_publish = date_publish
        self.deleted = deleted

    def __str__(self):
        return '<Article{}, {}, {}, {}, {}>'. \
            format(self.id, self.title, self.desc,
                   self.click_count, self.date_publish)

    def get_all(self, page_no, page_size=10):
        articles = db.session.query(Article).filter_by().paginate(page_no, page_size, False)
        return articles

    def get_by_id(self, id):
        article = db.session.query(Article).filter_by(id=id)
        return article

    def insert(self, article):
        db.session.add(article)
        session_commit()

    def delete(self, id):
        db.session.query(Article).filter_by(id=id).\
            update({'deleted': Constant.deleted.value, 'date_publish': time.time()})
        session_commit()

    def update(self, article):
        db.session.query(Article).filter_by(id=article.id).\
            update({'title': article.title, 'desc': article.desc, 'content': article.content,
                    'date_publish': article.date_publish})




def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
