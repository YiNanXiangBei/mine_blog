# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 上午11:20
# @filename: article.py
from flask import render_template

from application import app


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()

