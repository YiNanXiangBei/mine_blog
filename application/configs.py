from datetime import timedelta

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/mine_blog"
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = 'jwt_secret'
JWT_AUTH_URL_RULE = '/api/v1/auth'
JWT_EXPIRATION_DELTA = timedelta(seconds=120)
GITHUB_OAUTH = {
    'CLIENT_ID': 'f9fa118d12389497686b',
    'CLIENT_SECRET': 'a67149f74ce50c1e95c2d9bdeba7bbd579eb8d45',
    'AUTHORIZE_PATH': 'https://github.com/login/oauth/authorize',
    'ACCESS_TOKEN_PATH': 'https://github.com/login/oauth/access_token',
    'USER_MESSAGE_PATH': 'https://api.github.com/user',
}
