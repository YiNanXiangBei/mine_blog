# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午1:35
# @filename: article.py
import datetime

from sqlalchemy.exc import SQLAlchemyError

from application import db, app
from application.constant.constant import Constant
from application.models.comment import Comment
from application.models.tag_article import TagArticle


class Article(db.Model):
    __tablename__ = 'blog_article'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    desc = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.TEXT, nullable=False)
    click_count = db.Column(db.BigInteger, nullable=False, default=0)
    date_publish = db.Column(db.TIMESTAMP, nullable=False)
    deleted = db.Column(db.String(1), nullable=False, default='0')
    back_img = db.Column(db.String(200))
    # 在Comment中添加一个属性为article
    comments = db.relationship('Comment', backref=db.backref('article'))

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
        """
        分页查询文章数据，不用返回评论数据
        :param page_no:
        :param page_size:
        :return:
        """
        app.logger.info("get article by paginate ....")
        articles = db.session.query(Article).filter_by(deleted=Constant.UN_DELETED.value). \
            paginate(page_no, page_size, False)
        return articles

    @staticmethod
    def get_all_by_date(start_time, end_time, page_no, page_size=10):
        """
        依据日期进行分页查询
        :param start_time: 开始日期
        :param end_time: 结束日期
        :param page_no: 页号
        :param page_size: 总页数
        :return:
        """
        app.logger.info('get article by paginate and datetime ....')
        articles = db.session.query(Article).filter(Article.deleted == Constant.UN_DELETED.value,
                                                    Article.date_publish.between(start_time, end_time)).order_by(Article.date_publish.desc()).paginate(
            int(page_no), int(page_size), False)
        return articles

    @staticmethod
    def get_by_id(article_id):
        """
        依据文章id查询文章以及分页查询文章的评论
        :param article_id: 文章id
        :return: 文章及评论
        """
        app.logger.info("get article by id ....")
        article = db.session.query(Article).filter_by(id=article_id, deleted=Constant.UN_DELETED.value).first()
        return article

    @staticmethod
    def insert(article, tags_id):
        """
        插入文章
        :param article: 文章
        :param tags_id: 标签id
        :return:
        """
        app.logger.info("insert article ....")
        db.session.add(article)
        article_id = Article.get_id_by_title(article.title).id
        for tag_id in tags_id:
            tag_article = TagArticle(tag_id, article_id)
            TagArticle.save(tag_article)
        if TagArticle.session_commit() is None:
            return session_commit()
        db.session.rollback()

    @staticmethod
    def get_id_by_title(title):
        """
        通过文章标题获取id
        :param title:
        :return:
        """
        app.logger.info("get id by title ...")
        article = db.session.query(Article).filter_by(title=title).first()
        return article

    @staticmethod
    def delete(article_id):
        """
        删除文章
        :param article_id:文章id
        :return:
        """
        app.logger.info("delete article ....")
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        db.session.query(Article).filter_by(id=article_id). \
            update({'deleted': Constant.DELETED.value, 'date_publish': now})
        return session_commit()

    @staticmethod
    def update(article, tags_id):
        """
        更新文章
        :param article: 文章信息
        :param tags_id: 标签id
        :return:
        """
        app.logger.info("update article ....")
        # 先删除 tag_article表数据
        TagArticle.delete(article.id)
        # 再插入新的数据
        for tag_id in tags_id:
            tag_article = TagArticle(tag_id, article.id)
            TagArticle.save(tag_article)
        if TagArticle.session_commit() is None:
            db.session.query(Article).filter_by(id=article.id). \
                update({'title': article.title, 'desc': article.desc, 'content': article.content,
                        'date_publish': article.date_publish})
            return session_commit()
        db.session.rollback()


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
