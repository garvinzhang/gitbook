#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import List, Tuple

import requests


class QywxRobot(object):
    """QywxRobot

    Args:
        robotKey (str): asfda

    Attributes:
        SendMsg: asdsa
    """

    def __init__(self, robotKey: str) -> None:
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robotKey

    def SendMsg(
        self,
        content: str,
        msgType: str = "text",
        mentionedList: List[str] = [],
    ) -> Tuple[bool, str]:
        """SendMsg

        Args:
            content (str): message
            msgType (str="text"): text markdown
            mentionedList (List[str]=[]): ex ["vhukzhang","@all"]

        Returns:
            ok (bool): True
            err (str): msg
        """
        ok = False
        err = ""
        headers = {"Content-Type": "application/json"}
        if msgType == "markdown":
            mentionedText = []
            for mentioned in mentionedList:
                if mentioned == "@all":
                    continue
                mentionedText.append(f"<@{mentioned}>")
            data = {
                "msgtype": msgType,
                msgType: {"content": content + "\n" + "".join(mentionedText)},
            }
        else:
            msgType = "text"
            data = {
                "msgtype": msgType,
                msgType: {
                    "content": content,
                    "mentioned_list": mentionedList,
                },
            }
        rsp = requests.post(
            url=self.url,
            headers=headers,
            data=json.dumps(data),
        )
        if rsp.status_code == 200 and rsp.text == '{"errcode":0,"errmsg":"ok"}':
            ok = True
        else:
            err = str(rsp.status_code) + " | " + rsp.text
        return ok, err
