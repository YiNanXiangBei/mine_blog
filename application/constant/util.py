# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-17 下午9:38
# @filename: util.py
import base64

import os

from application import app
import time
import re
from io import BytesIO

from PIL import Image
from qcloud_cos import CosConfig, CosS3Client

from application import configs

import smtplib
from email.header import Header  # 用来设置邮件头和邮件主题
from email.mime.text import MIMEText  # 发送正文只包含简单文本的邮件，引入MIMEText即可
import logging

logger = logging.getLogger("email_log")
logger.setLevel(logging.DEBUG)

# 输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# 输出到文件
fh = logging.FileHandler("log.log")
fh.setLevel(logging.INFO)
# 设置日志格式
fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
ch.setFormatter(fomatter)
fh.setFormatter(fomatter)
logger.addHandler(ch)
logger.addHandler(fh)


class CommonUtil(object):
    @staticmethod
    def handle_img(base64_str, filename):
        image_path = configs.SYS_UPLOAD_PATH + filename
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        if image_path:
            img.convert("RGB").save(image_path, 'WEBP')
        return img

    @staticmethod
    def upload_img(filename):
        tencent_config = configs.TENCENT_OAUTH
        image_path = configs.SYS_UPLOAD_PATH + filename
        config = CosConfig(Region=tencent_config.get('region'), Secret_id=tencent_config.get('secret_id'),
                           Secret_key=tencent_config.get('secret_key'))  # 获取配置对象
        client = CosS3Client(config)
        remote_name = str(int(time.time())) + '.webp'
        remote_url = 'http://{}.cosgz.myqcloud.com/{}'.format(tencent_config.get('bucket'), remote_name)
        response = None
        try:
            with open(image_path, 'rb') as fp:
                response = client.put_object(
                    Bucket=tencent_config.get('bucket'),
                    Body=fp.read(),
                    Key=remote_name
                )
            os.remove(image_path)
        except Exception as e:
            app.logger.error('upload file to tencent error: {}'.format(e))
        if response is not None and response['ETag'] is not None:
            return remote_url
        else:
            return None

    @staticmethod
    def sendEmail(receiver):
        mail_config = configs.EMAIL_OAUTH
        sender = mail_config.get('sender')
        # receiver = '2043281367@qq.com'

        # 所使用的用来发送邮件的SMTP服务器
        smtpServer = mail_config.get('smtpServer')

        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        username = mail_config.get('username')
        password = mail_config.get('password')

        mail_title = '2018.7.23邮件测试'
        mail_body = '邮件测试'

        # 创建一个实例
        message = MIMEText(mail_body, 'plain', 'utf-8')  # 邮件正文
        message['From'] = sender  # 邮件上显示的发件人
        message['To'] = receiver  # 邮件上显示的收件人
        message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题

        try:
            smtp = smtplib.SMTP()  # 创建一个连接
            smtp.connect(smtpServer)  # 连接发送邮件的服务器
            smtp.login(username, password)  # 登录服务器
            smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
            logger.info("邮件发送成功！！！")
            print("邮件发送成功！！！")
            smtp.quit()
        except smtplib.SMTPException:
            logger.info("邮件发送失败！！！")
            print("邮件发送失败！！！")