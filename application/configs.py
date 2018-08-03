from datetime import timedelta

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/mine_blog"
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = 'jwt_secret'
JWT_AUTH_URL_RULE = '/api/v1/auth'
JWT_EXPIRATION_DELTA = timedelta(seconds=12000)
SYS_UPLOAD_PATH = '/home/laowang/gitwarehouse/mine_blog/application/static/img/'
GITHUB_OAUTH = {
    'CLIENT_ID': 'f9fa118d12389497686b',
    'CLIENT_SECRET': 'a67149f74ce50c1e95c2d9bdeba7bbd579eb8d45',
    'AUTHORIZE_PATH': 'https://github.com/login/oauth/authorize',
    'ACCESS_TOKEN_PATH': 'https://github.com/login/oauth/access_token',
    'USER_MESSAGE_PATH': 'https://api.github.com/user',
}
TENCENT_OAUTH = {
    'secret_id': '',
    'secret_key': '',
    'region': '',
    'bucket': ''
}
EMAIL_OAUTH = {
    # 发件人
    'sender': '',
    # 所使用的用来发送邮件的SMTP服务器
    'smtpServer': 'smtp.163.com',
    # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
    'username': '',
    'password': ''
}

ENCRYPT_KEY = {
    # 公钥
    'public_key': """""",
    # 私钥
    'private_key': """"""
}