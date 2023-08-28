#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
首码网的数据 作为广告数据交付

湖南省企业匹配 写入到落地页的kafka 发一下机器人吧
"""
import os
import sys

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)
print(lib_path)

from base.utils import get_logger

logger = get_logger()
