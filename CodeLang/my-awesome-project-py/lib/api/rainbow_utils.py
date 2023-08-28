#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import Any, Dict, NamedTuple, List

import yaml
from rainbow_sdk.rainbow_client import RainbowClient


class RainbowConf(NamedTuple):
    app_id: str
    user_id: str
    secret_key: str
    group: str
    env_name: str


class RainbowUtils:
    def __init__(self, rainbow_conf: RainbowConf) -> None:
        init_param = {
            "connectStr": "api.rainbow.oa.com:8080",
            "tokenConfig": {
                "app_id": rainbow_conf.app_id,
                "user_id": rainbow_conf.user_id,
                "secret_key": rainbow_conf.secret_key,
            },
        }
        rainbow_client = RainbowClient(init_param)
        self.res = rainbow_client.get_configs_v3(
            group=rainbow_conf.group,
            env_name=rainbow_conf.env_name,
        )

    def parse_json(self, key: str) -> Dict[str, Any]:
        data = json.loads(self.res["data"][key])
        return data

    def parse_yaml(self, key: str) -> Dict[str, Any]:
        data = yaml.safe_load(self.res["data"][key])
        # try:
        #     with open(yaml_path, "r") as conf:
        #         yaml_map = yaml.safe_load(conf)
        # except FileNotFoundError:
        #     err = "ConfigFileNotFound:" + yaml_path
        # except Exception as ex:
        #     err = "UnknownErr:" + str(ex)
        return data

    def parse_stopwords(self, key: str = "stopwords") -> List[str]:
        data_ori = self.res["data"][key]
        data_lst = data_ori.split("\n")
        stopwords = []
        for data in data_lst:
            word = data.replace("\n", "").replace("\r", "").strip()
            if word:
                stopwords.append(word)
        return stopwords
