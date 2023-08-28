#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR)

from tools.fast_log import FastLog
from tools.cos import Cos, CosConf
from tools.rainbow import Rainbow
from tools.mysql import Mysql, MysqlConf
from tools.redis import Redis, RedisConf
from tools.qywx_robot import QywxRobot

FAST_LOG = FastLog()


def GetFastLog(file: str):
    fastLog = FAST_LOG.GetLogger(
        f"{DIR}/log/{file.split('/')[-1].replace('.py','')}.log"
    )
    return fastLog


init_log = GetFastLog(__file__)

# init rainbow
init_log.info("rainbow")
RAINBOW = Rainbow(
    appId="c228a2d5-bfcb-4ba5-b13e-63b439a94675",
    userId="d8a0159e3e554f90b700fdfeff084b01",
    secretKey="15f855d2d510d357bdbf8bb2ba86a8dfaa9a",
    group="vhukzhang",
    envName="Default",
)
ok, err = RAINBOW.Init()
if not ok:
    init_log.error(err)
    raise

# init mysql
init_log.info("mysql")
rMysql = RAINBOW.GetValue("mysql")
mysqlConf = MysqlConf(
    host=rMysql["write_22398"]["host"],
    user=rMysql["write_22398"]["user"],
    password=rMysql["write_22398"]["password"],
    port=rMysql["write_22398"]["port"],
)
MYSQL = Mysql(mysqlConf=mysqlConf)

# init redis
init_log.info("redis")
rRedis = RAINBOW.GetValue("redis")
redisConf = RedisConf(
    host=rRedis["crs-qgyf8r1r"]["host"],
    port=rRedis["crs-qgyf8r1r"]["port"],
    password=rRedis["crs-qgyf8r1r"]["password"],
    db=8,
)
REDIS = Redis(redisConf=redisConf)

# init Cos
init_log.info("fastCos")
rCos = RAINBOW.GetValue("cos")
cosConf = CosConf(
    bucketName="middle-collection",
    bucketId=rCos["urlsafe"]["bucketId"],
    secretKey=rCos["urlsafe"]["secretKey"],
    secretId=rCos["urlsafe"]["secretId"],
    region="ap-guangzhou",
)
COS = Cos(cosConf=cosConf)

# init qywxRobot
init_log.info("qywxRobot")
QYWX_ROBOT = QywxRobot("d940479c-298b-4fdd-9989-dea51eccabca")


class InitAll(object):
    def __init__(self) -> None:
        self.MYSQL = MYSQL
        self.REDIS = REDIS
        self.COS = COS
        self.QYWX_ROBOT = QYWX_ROBOT


INIT_ALL = InitAll()
