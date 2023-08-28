#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)
print(lib_path)

from api.qywx_robot import robot_send_msg
from base.utils import get_logger
from spec.config import get_config

logger = get_logger()


class TestDemo(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = get_config()

    def test_logger(self):
        logger.info("test")

    def test_demo(self):
        logger.info("demo")
        robot_send_msg(content="test", robot_key=self.config.secret_robot.chatgpt)


if __name__ == "__main__":
    unittest.main()
