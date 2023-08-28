#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR)

from tools.tests.test_init import INIT_ALL, GetFastLog

test_log = GetFastLog(__file__)



class TestRedis(object):
    def test_list(self):
        dictStr = {"test1": 123, "test2": True, "test3": "abc"}
        ok, data, err = INIT_ALL.REDIS.ListUtil(
            action="lpush",
            keyName="test",
            value=dictStr,
            ex=2,
        )
        if not ok:
            test_log.error(data)
            test_log.info(err)
            return

        ok, data, err = INIT_ALL.REDIS.ListUtil(action="lpop", keyName="test", value="")
        if not ok:
            test_log.error(data)
            test_log.info(err)
            return

        test_log.info(data)

        ok, data, err = INIT_ALL.REDIS.ListUtil(
            action="blpop", keyName="test", value=""
        )
        if not ok:
            test_log.error(data)
            test_log.info(err)
            return

        test_log.info(data)

    def test_filter(self):
        ok = INIT_ALL.REDIS.StrFilter("filter", 8)
        test_log.info(ok)

    def test_close(self):
        ok, err = INIT_ALL.REDIS.CloseConn()
        test_log.info(ok)
        test_log.info(err)

    def test_ping(self):
        ok, err = INIT_ALL.REDIS.PingConn()
        test_log.info(ok)
        test_log.info(err)

    # def redisUtil(self):
    #     self.redisConn = redis.Redis(connection_pool=self.pool)
    #     self.redisConn.delete("s")
    #     self.redisConn.exists("ss")
    #     self.redisConn.randomkey()
    #     self.redisConn.llen("ss")
    #     self.redisConn.get("ss")
    #     self.redisConn.keys()
    #     self.redisConn.dbsize()
    #     # 若寻求更高效率的批量redis操作，可以使用管道的方式
    #     pipe = self.redisConn.pipeline()
    #     pipe.set("name", "jack")
    #     pipe.set("role", "sb")
    #     pipe.sadd("faz", "baz")
    #     pipe.incr("num")
    #     pipe.execute()  # 管道操作提交


TEST_REDIS = TestRedis()

TEST_REDIS.test_ping()

TEST_REDIS.test_filter()
TEST_REDIS.test_filter()

TEST_REDIS.test_list()

TEST_REDIS.test_close()

TEST_REDIS.test_ping()

TEST_REDIS.test_filter()
