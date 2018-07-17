# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-17 下午9:38
# @filename: util.py
import base64
import re
from io import BytesIO

from PIL import Image


class CommonUtil(object):
    @staticmethod
    def handle_img(base64_str, filename):
        image_path = '/home/laowang/gitwarehouse/mine_blog/application/static/img/{}'.format(filename)
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        if image_path:
            img.convert("RGB").save(image_path, 'WEBP')
        return img
