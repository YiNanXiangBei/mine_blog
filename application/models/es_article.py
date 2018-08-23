# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-20 下午1:58
# @filename: es_article.py
from elasticsearch import Elasticsearch

from application import configs, app


class EsArticle(object):
    def __init__(self, ip):
        self.es = Elasticsearch([ip], http_auth=(configs.ES_CONFIG.get('username'), configs.ES_CONFIG.get('password')),
                                port=configs.ES_CONFIG.get('port'))

    def get_articles(self, search_params):
        """
        去es中查询数据
        :param search_params:
        :return:
        """
        search_params = {
            "query": {
                "bool": {
                    "must": {
                        "dis_max": {
                            "queries": [
                                {"match": {"title": search_params}},
                                {"match": {"content": search_params}}
                            ]
                        }
                    },
                    "filter": {
                        "term": {"deleted": 0}
                    }
                }
            },
            "highlight": {
                "pre_tags": ["<tag1>", "<tag2>"],
                "post_tags": ["</tag1>", "</tag2>"],
                "fields": {
                    "title": {},
                    "content": {}
                }
            }
        }
        config = configs.ES_CONFIG
        all_articles = None
        try:
            all_articles = self.es.search(index=config.get('index'), doc_type=config.get('type'), body=search_params)
        except Exception as e:
            app.logger.error("get data from es error: {}".format(e))
        return all_articles

