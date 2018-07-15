from flask import render_template

from application import app


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/person')
def person():
    return render_template("404.html")


if __name__ == '__main__':
    app.run()
