#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys

import requests

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)

from base.utils import UtilsError


def robot_send_msg(content: str, robot_key: str):
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robot_key
    headers = {"Content-Type": "application/json"}
    msg_type = "text"
    data = {
        "msgtype": msg_type,
        msg_type: {
            "content": content,
            "mentioned_list": [],
        },
    }
    rsp = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=3,
    )
    if rsp.status_code != 200 or rsp.text != '{"errcode":0,"errmsg":"ok"}':
        err = f"content:{content}|robot_key:{robot_key}|code:{str(rsp.status_code)}|text:{rsp.text}"
        raise UtilsError(err)
