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
