#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from typing import NamedTuple

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)

from api.cos_utils import CosConf
from api.rainbow_utils import RainbowConf, RainbowUtils
from base.mysql_utils import MysqlConf
from base.redis_utils import RedisConf


class PwdMysql(NamedTuple):
    financial_v2: MysqlConf
    urlsec: MysqlConf
    regbase: MysqlConf
    urlyuqing: MysqlConf
    urldata: MysqlConf
    adcollection: MysqlConf


class PwdRedis(NamedTuple):
    vhukzhang_wxmp: RedisConf
    vhukzhang_test: RedisConf
    vhukzhang_chuanxiao: RedisConf


class SecretCos(NamedTuple):
    lingkun: CosConf


class SecretRobot(NamedTuple):
    chatgpt: str


class Config(NamedTuple):
    pwd_mysql: PwdMysql
    pwd_redis: PwdRedis
    secret_cos: SecretCos
    secret_robot: SecretRobot


def get_config() -> Config:
    rainbow_conf = RainbowConf(
        app_id="892cc757-e4fc-4875-898b-3577b5e9cc8d",
        user_id="b1dc6f40fb69462cb94778b420dadb39",
        secret_key="0b2398cd2e9befd71acde68dbfb974909d92",
        group="financial_model_proj",
        env_name="Default",
    )
    rainbow_utils = RainbowUtils(rainbow_conf=rainbow_conf)

    pwd_mysql_json = rainbow_utils.parse_json(key="pwd.mysql")
    pwd_mysql = PwdMysql(
        financial_v2=MysqlConf(**pwd_mysql_json["financial_v2"]),
        urlsec=MysqlConf(**pwd_mysql_json["urlsec"]),
        regbase=MysqlConf(**pwd_mysql_json["regbase"]),
        urlyuqing=MysqlConf(**pwd_mysql_json["urlyuqing"]),
        urldata=MysqlConf(**pwd_mysql_json["urldata"]),
        adcollection=MysqlConf(**pwd_mysql_json["adcollection"]),
    )

    pwd_redis_json = rainbow_utils.parse_json(key="pwd.redis")
    pwd_redis = PwdRedis(
        vhukzhang_wxmp=RedisConf(**pwd_redis_json["vhukzhang_wxmp"]),
        vhukzhang_test=RedisConf(**pwd_redis_json["vhukzhang_test"]),
        vhukzhang_chuanxiao=RedisConf(**pwd_redis_json["vhukzhang_chuanxiao"]),
    )

    secret_cos_json = rainbow_utils.parse_json(key="secret.cos")
    secret_cos = SecretCos(
        lingkun=CosConf(**secret_cos_json["lingkun"]),
    )

    secret_robot_json = rainbow_utils.parse_json(key="secret.robot")
    secret_robot = SecretRobot(
        chatgpt=secret_robot_json["chatgpt"],
    )

    rainbow_config = Config(
        pwd_mysql=pwd_mysql,
        pwd_redis=pwd_redis,
        secret_cos=secret_cos,
        secret_robot=secret_robot,
    )

    return rainbow_config
