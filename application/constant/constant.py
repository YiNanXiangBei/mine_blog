# -*- coding: utf8 -*-
# @author: yinan
# @time: 18-7-3 下午9:37
# @filename: constant.py
"""
常量存储位置
"""
from enum import Enum, unique


@unique
class Constant(Enum):
    deleted = '1'
