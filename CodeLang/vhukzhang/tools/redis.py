#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NamedTuple, Any, Tuple
import json

import redis


class RedisConf(NamedTuple):
    """RedisConf

    redis 连接所需的参数
    """

    host: str
    port: int
    password: str
    db: int


class Redis(object):
    def __init__(self, redisConf: RedisConf) -> None:
        self.redisConn = redis.Redis(
            host=redisConf.host,
            port=redisConf.port,
            password=redisConf.password,
            db=redisConf.db,
        )

    def GetRedisConn(self):
        return self.redisConn

    def StrFilter(self, key: str, ex: int) -> bool:
        """Filter

        Args:
            key (str): ss
            ex (int): 10

        Returns:
            ok (bool): True说明已经有缓存, False说明无缓存并已加上缓存
        """
        ok = self.redisConn.set(name=key, value=1, ex=ex, nx=True)
        if not ok:
            ok = False
        return ok

    def ListUtil(
        self,
        action: str,
        keyName: str,
        value: Any,
        ex: int = 2,
    ) -> Tuple[bool, Any, str]:
        """ListUtil

        Args:
            action (str): s
            keyName (str): s
            value (Any): s
            ex (int=2): ex

        Returns:
            ok (book): True
            data (Any): s
            err (str): s
        """
        ok = False
        data = None
        err = ""
        if action not in ("lpush", "rpush", "lpop", "rpop", "blpop", "brpop"):
            err = "Invalid action"
            return ok, data, err
        if action == "lpush":
            value = json.dumps(value)
            data = self.redisConn.lpush(keyName, value)
        elif action == "rpush":
            value = json.dumps(value)
            data = self.redisConn.rpush(keyName, value)
        elif action == "lpop":
            data = self.redisConn.lpop(keyName)
            data = json.loads(data)
        elif action == "rpop":
            data = self.redisConn.rpop(keyName)
            data = json.loads(data)
        elif action == "blpop":
            data = self.redisConn.blpop(keyName, timeout=ex)
            if data:
                data = json.loads(data)  # type: ignore
        elif action == "brpop":
            data = self.redisConn.brpop(keyName, timeout=ex)
            if data:
                data = json.loads(data)  # type: ignore
        ok = True
        return ok, data, err

    def CloseConn(self) -> Tuple[bool, str]:
        ok = False
        err = ""
        try:
            self.redisConn.close()
            ok = True
        except Exception as ex:
            err = str(ex)
        return ok, err

    def PingConn(self) -> Tuple[bool, str]:
        ok = False
        err = ""
        try:
            self.redisConn.ping()
            ok = True
        except redis.exceptions.ConnectionError as ex:
            err = str(ex)
        except Exception as ex:
            err = str(ex)
        return ok, err
