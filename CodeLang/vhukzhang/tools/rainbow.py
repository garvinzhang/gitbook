#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Tuple, Dict

import yaml
from rainbow_sdk.rainbow_client import RainbowClient


class Rainbow(object):
    """Rainbow

    Args:
        appId (str): 七彩石配置分组对应的appId
        userId (str): 用户Id
        secretKey (str): 密钥
        group (str): 分组名
        envName (str): 环境名

    Attributes:
        Init: s
        GetValue: asd
    """

    def __init__(
        self,
        appId: str,
        userId: str,
        secretKey: str,
        group: str,
        envName: str,
    ) -> None:
        self.group = group
        self.envName = envName
        self.init_param = {
            "connectStr": "api.rainbow.oa.com:8080",
            "tokenConfig": {
                "app_id": appId,
                "user_id": userId,
                "secret_key": secretKey,
            },
        }
        self.data_ori = {}

    def Init(self) -> Tuple[bool, str]:
        """init

        Args:
            None

        Returns:
            ok (bool): True or False
            err (str): 错误详情
        """
        ok = False
        err = ""
        res = {}
        for _ in range(3):
            rc = RainbowClient(self.init_param)
            res = rc.get_configs_v3(self.group, env_name=self.envName)
            if res["code"] == 0:
                ok = True
                self.data_ori = res["data"]
                break
        err = res.get("message", "")
        return ok, err

    def GetValue(self, key: str) -> Dict:
        """GetValue

        Args:
            key (str): 键

        Returns:
            value (Dict): 值
        """
        text = self.data_ori.get(key, "")
        value = yaml.safe_load(text)
        return value
