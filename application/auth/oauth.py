# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-5 下午2:31
# @filename: oauth.py
import json
import time

import requests
from flask import jsonify

from application import configs
from application.constant.constant import Constant
from application.models.user import User


class Oauth(object):
    client_id = None
    client_secret = None
    authorize_path = None
    access_token_path = None
    user_message_path = None

    def __init__(self):
        oauth_config = configs.GITHUB_OAUTH
        self.client_id = oauth_config.get("CLIENT_ID")
        self.client_secret = oauth_config.get("CLIENT_SECRET")
        self.authorize_path = oauth_config.get("AUTHORIZE_PATH")
        self.access_token_path = oauth_config.get("ACCESS_TOKEN_PATH")
        self.user_message_path = oauth_config.get("USER_MESSAGE_PATH")

    def get_redirect_path(self):
        return "{}?client_id={}&scope={}&state={}".\
            format(self.authorize_path, self.client_id, '[\'user\']', str(int(time.time())))

    def get_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code
        }
        response = requests.post(self.access_token_path, data=params)
        token = response.content.decode("utf-8").split("&")[0].split("=")[1]
        return token

    def get_user(self, code):
        token = self.get_token(code)
        path = "{}?access_token={}&scope={}".format(self.user_message_path, token, 'user')
        result = json.loads(requests.get(path).content.decode("utf-8"))
        if result is not None and len(result) > Constant.TWO.value:
            user = User(result['id'], result['login'], result['url'], result['avatar_url'])
            User.save(user)
        return jsonify(result)
