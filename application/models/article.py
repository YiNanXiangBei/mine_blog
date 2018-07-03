# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: article.py
from application import db


class Article(db.Model):
    __tablename__ = 'blog_article'
    id = db.Column(db.BIGINT(20), primary_key=True, nullable=False, unique=True)
    tag_id = db.Column(db.BIGINT(20), nullable=False)
    title = db.Column(db.String(50), nullable=False, unique=True)
    desc = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.TEXT, nullable=False)
    click_count = db.Column(db.BIGINT(20), nullable=False, default=0)
    date_publish = db.Column(db.TIMESTAMP, nullable=False)
    # 在Comment中添加一个属性为article
    comments = db.relationship('Comment', backref='article')

    def __init__(self, tag_id, title, desc, content, click_count, date_publish):
        self.tag_id = tag_id
        self.title = title
        self.desc = desc
        self.content = content
        self.click_count = click_count
        self.date_publish = date_publish

    def __str__(self):
        return '<Article{}, {}, {}, {}, {}, {}>'. \
            format(self.id, self.tag_id, self.title, self.desc,
                   self.click_count, self.date_publish)

    def get_all(self, page_no, page_size=10):
        articles = db.session.query(Article).filter_by().paginate(page_no, page_size, False)
        return articles

    def get_by_id(self, id):
        article = db.session.query(Article).filter_by(id=id)
        return article
