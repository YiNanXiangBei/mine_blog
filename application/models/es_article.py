# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-20 下午1:58
# @filename: es_article.py
from elasticsearch import Elasticsearch

from application import configs


class EsArticle(object):
    def __init__(self, ip="127.0.0.1"):
        self.es = Elasticsearch([ip])

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
        all_articles = self.es.search(index=config.get('index'), doc_type=config.get('type'), body=search_params)
        return all_articles

