# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-8-2 下午2:46
# @filename: client_controller.py
from flask import Blueprint, request, jsonify

from application.auth.decrypt import decrypt

client = Blueprint('/', __name__)


@client.route('/index', methods=['GET'])
@decrypt
def index(message):
    return jsonify(message)
