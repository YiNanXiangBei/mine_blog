# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-17 下午9:38
# @filename: util.py
import base64

import os
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
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
import rsa

# logger = logging.getLogger("email_log")
# logger.setLevel(logging.DEBUG)
#
# # 输出到屏幕
# ch = logging.StreamHandler()
# ch.setLevel(logging.WARNING)
# # 输出到文件
# fh = logging.FileHandler("log.log")
# fh.setLevel(logging.INFO)
# # 设置日志格式
# fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
# ch.setFormatter(fomatter)
# fh.setFormatter(fomatter)
# logger.addHandler(ch)
# logger.addHandler(fh)
from application.configs import ENCRYPT_KEY


class CommonUtil(object):
    @staticmethod
    def handle_img(base64_str, filename):
        """
        将base64位数据转换成web格式图片
        :param base64_str:
        :param filename:
        :return:
        """
        image_path = configs.SYS_UPLOAD_PATH + filename + '.png'
        webp_path = configs.SYS_UPLOAD_PATH + filename + '.webp'
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        if webp_path:
            img.convert("RGB").save(webp_path, 'WEBP')
        if image_path:
            img = Image.open(webp_path).save(image_path, 'PNG')
        return img

    @staticmethod
    def upload_img(filename, img_type='.webp'):
        """
        将图片上传到云存储中
        :param filename:
        :param img_type:
        :return:
        """
        tencent_config = configs.TENCENT_OAUTH
        image_path = configs.SYS_UPLOAD_PATH + filename
        config = CosConfig(Region=tencent_config.get('region'), Secret_id=tencent_config.get('secret_id'),
                           Secret_key=tencent_config.get('secret_key'))  # 获取配置对象
        client = CosS3Client(config)
        remote_name = str(int(time.time())) + img_type
        remote_url = '{}/{}'.format(configs.SYS_IMG_URL, remote_name)
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
    def send_email(receiver, sid):
        mail_config = configs.EMAIL_OAUTH
        sender = mail_config.get('sender')
        # receiver = '2043281367@qq.com'

        # 所使用的用来发送邮件的SMTP服务器
        smtp_server = mail_config.get('smtpServer')

        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        username = mail_config.get('username')
        password = mail_config.get('password')

        mail_title = '找回密码'
        mail_body = '''
        <h3>亲爱的用户：</h3>
        <p>请您在24小时之内点击下面的链接修改登录密码</p>
        <p><a href="http://127.0.0.1:8080/sysadmin/password_change?sid={}">http://127.0.0.1:8080/sysadmin/password_change?sid={}</a></p>
        <p>若链接点击无效，请复制链接到浏览器地址栏打开</p>
        <p>若您未申请密码修改，请忽略此邮件</p>
        '''

        # 创建一个实例
        message = MIMEText(mail_body.format(sid,sid), 'html', 'utf-8')  # 邮件正文
        message['From'] = sender  # 邮件上显示的发件人
        message['To'] = receiver  # 邮件上显示的收件人
        message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题

        try:
            smtp = smtplib.SMTP()  # 创建一个连接
            smtp.connect(smtp_server)  # 连接发送邮件的服务器
            smtp.login(username, password)  # 登录服务器
            smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
            app.logger.info("邮件发送成功！！！")
            # print("邮件发送成功！！！")
            smtp.quit()
        except smtplib.SMTPException as e:
            app.logger.info("邮件发送失败！！！")
            return str(e)
            # print("邮件发送失败！！！")

    @staticmethod
    def encrypt(params):
        """
        数据加密
        :param params:
        :return:
        """
        signature = rsa.sign(params.encode(), ENCRYPT_KEY.get('public_key'), 'SHA-1')
        data = {
            'params': params,
            'signature': signature
        }
        return rsa.encrypt(str(data).encode(), ENCRYPT_KEY.get('private_key'))

    @staticmethod
    def rsa_decrypt(private_key, biz_content):
        """
        数据解密 最大长度117
        :param private_key:
        :param biz_content:
        :return:
        """
        rsakey = RSA.importKey(private_key)  # 导入读取到的私钥
        cipher = PKCS1_v1_5.new(rsakey)  # 生成对象
        try:
            biz_content = base64.b64decode(biz_content)
            # 1024bit key
            default_length = 344
            len_content = len(biz_content)
            if len_content <= default_length:
                return cipher.decrypt(base64.b64decode(bytes.fromhex(biz_content.decode()).decode()), None).decode()
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_length:
                    params_lst.append(
                        cipher.decrypt(base64.b64decode(
                            bytes.fromhex(biz_content[offset: offset + default_length].decode()).decode()),
                                       None).decode())
                else:
                    params_lst.append(
                        cipher.decrypt(base64.b64decode(bytes.fromhex(biz_content[offset:].decode()).decode()),
                                       None).decode())
                offset += default_length
            target = ''.join(params_lst)
            return target
        except Exception as e:
            app.logger.error('rsa decrypt error: {}'.format(e))
            return None

    @staticmethod
    def aes_decrypt(key, params):
        """
        aes解密
        :param key: 字符串类型密钥
        :param params: 十六进制的字符串，需要转为二进制字节数组
        :return:
        """
        # 解密的话要用key和iv生成新的AES对象
        try:
            iv = bytes.fromhex(params[:32])
            params = bytes.fromhex((params[32:]))
            my_decrypt = AES.new(key, AES.MODE_CBC, iv)
            # 使用新生成的AES对象，将加密的密文解密
            decrypt_text = _unpad(my_decrypt.decrypt(params))
            return decrypt_text.decode()
        except Exception as e:
            app.logger.error('aes decrypt error: {}'.format(e))


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]