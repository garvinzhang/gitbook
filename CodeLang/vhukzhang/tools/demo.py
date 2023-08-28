#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR)

from tools.fast_log import FastLog

FAST_LOG = FastLog()
test_log = FAST_LOG.GetLogger(f"{DIR}/tmp/log/test.log")

test_log.info("demo")
