#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)
print(lib_path)

from base.utils import get_logger

logger = get_logger()


class TestDemo(unittest.TestCase):
    def test_logger(self):
        logger.info("test")

    def test_conver(self):
        txt = "'fasf\\tasedf\asdas\easf"
        logger.info(txt)
        logger.info(txt.encode("unicode_escape").decode("ascii"))


if __name__ == "__main__":
    unittest.main()
