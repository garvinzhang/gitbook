#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR)

from init import GetFastLog, INIT_ALL

fastLog = GetFastLog(__file__)


fastLog.info("demo")

# 新业态数据流 TODO(vhukzhang): sss
"""
字段对齐
H01
M01
W01

梳理干净 找到可以优化的地方
"""
