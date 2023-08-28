#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)
print(lib_path)

from base.utils import get_logger
from base.mysql_utils import MysqlConf,MysqlUtils

logger = get_logger()


class TestDemo(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.a = "hello"
        logger.info(methodName)

    def test_logger(self):
        logger.info("test")
        logger.info(self.a)

    def test_mysql(self):
        mysql_conf = MysqlConf(host="12.42.24.122",user="writeuser",password="^1asdfasn187",port=3306)
        logger.info(mysql_conf)
        mysql_utils = MysqlUtils(mysql_conf=mysql_conf) # 实丽华、初始化 __init__ connection

        sql = "SELECT * FROM table"
        datas = mysql_utils.get_datas(sql=sql)
        for data in datas:
            logger.info(data)



if __name__ == "__main__":
    unittest.main()
