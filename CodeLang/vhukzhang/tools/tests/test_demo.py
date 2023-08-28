#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR)

from tools.tests.test_init import INIT_ALL, GetFastLog

test_log = GetFastLog(__file__)


test_log.info("demo")
