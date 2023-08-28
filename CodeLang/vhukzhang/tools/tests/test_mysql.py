#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR)

from tools.tests.test_init import INIT_ALL, GetFastLog

test_log = GetFastLog(__file__)


class TestMysql(object):
    def test_select(self):
        sqlStr = "SELECT * FROM audit.audit_new_industry_model_result ORDER BY RAND() LIMIT 20"
        ok, datas, err = INIT_ALL.MYSQL.Select(sqlStr=sqlStr)
        test_log.info(ok)
        test_log.info(err)
        for data in datas:
            test_log.info(data)
            break

    def test_ping(self):
        ok, err = INIT_ALL.MYSQL.PingConn()
        test_log.info(ok)
        test_log.info(err)

    def test_close(self):
        ok, err = INIT_ALL.MYSQL.CloseConn()
        test_log.info(ok)
        test_log.info(err)


TEST_MYSQL = TestMysql()
TEST_MYSQL.test_ping()

TEST_MYSQL.test_select()

TEST_MYSQL.test_close()

TEST_MYSQL.test_ping()

TEST_MYSQL.test_select()
