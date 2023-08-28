#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from typing import NamedTuple, List, Dict, Any

import pymysql

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)

from base.utils import get_logger, conver_str, UtilsError

logger = get_logger()


class MysqlConf(NamedTuple):
    host: str
    user: str
    password: str
    port: int


class MysqlUtils:
    def __init__(self, mysql_conf: MysqlConf) -> None:
        self.mysql_conn = pymysql.connect(
            host=mysql_conf.host,
            user=mysql_conf.user,
            password=mysql_conf.password,
            port=mysql_conf.port,
        )

    def get_datas(self, sql: str):
        cursor = self.mysql_conn.cursor()
        cursor.execute(sql)
        self.mysql_conn.commit()
        datas = cursor.fetchall()
        cursor.close()
        return datas

    def save_datas(
        self,
        table: str,
        datas: List[Dict[str, Any]],
        update: bool = False,
    ):
        if not datas:
            err = f"table:{table}|datas:{datas}|EMPTY DATAS"
            raise UtilsError(err)

        cursor = self.mysql_conn.cursor()

        for data in datas:
            key_list = []
            value_list = []
            append_list = []
            for key, value in data.items():
                append_list.append(f"{key}=VALUES({key})")
                key_list.append(key)
                if isinstance(value, str):
                    value = conver_str(origin_str=value)
                value_list.append(f"'{value}'")
            save_sql = f"INSERT INTO {table} ({','.join(key_list)}) VALUES ({','.join(value_list)})"
            append_sql = ""
            if update:
                append_sql = f" ON DUPLICATE KEY UPDATE {','.join(append_list)}"
            save_sql += append_sql

            cursor.execute(save_sql)

        self.mysql_conn.commit()
        cursor.close()
