#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os
import re
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Dict, Literal

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
log_file_default = f"{os.path.dirname(lib_path)}/log/default.log"


class UtilsError(Exception):
    pass


def get_logger(
    log_file: str = log_file_default,
    log_level: Literal["debug", "info", "warning", "error", "critical"] = "debug",
    log_console: bool = True,
    log_keep_days: int = 3,
) -> logging.Logger:
    """get_logger

    Args:
        log_file: s
        log_level: debug info warning error critical
        log_console: s
        log_keep_days: keep days

    Returns:
        logger: s
    """
    logger = logging.getLogger(log_file)

    formatter = logging.Formatter(
        "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    logger_level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }
    logger.setLevel(logger_level_map[log_level])

    if log_console:
        log_screen = logging.StreamHandler()
        log_screen.setFormatter(formatter)
        logger.addHandler(log_screen)

    try:
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="MIDNIGHT",
            interval=1,
            backupCount=log_keep_days,
        )
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except FileNotFoundError:
        pass
    return logger


def get_time(
    time_type: Literal["datetime", "date", "ds"] = "datetime",
    back_day: int = 0,
    round_time: bool = False,
) -> str:
    """get_time

    根据传入参数返回相应格式的时间

    Args:
        time_type: 日期时间格式，支持"datetime"(默认)、"date"、"ds"三种格式
        back_day: "datetime"和"date"格式下时间往前推的天数，默认为0
        round_time: 是否将时间戳改为0点

    Returns:
        返回字符串类型的时间
    """
    if time_type == "datetime":
        if round_time:
            return (datetime.now() - timedelta(back_day)).strftime("%Y-%m-%d 00:00:00")
        return (datetime.now() - timedelta(back_day)).strftime("%Y-%m-%d %H:%M:%S")
    elif time_type == "date":
        return (datetime.now() - timedelta(back_day)).strftime("%Y-%m-%d")
    elif time_type == "ds":
        return (datetime.now() - timedelta(back_day)).strftime("%Y%m%d")


def clean_dict_type(
    row_dict: Dict[str, Any],
    key_type_map: Dict[str, str],
) -> Dict[str, Any]:
    """clean_dict_type

    在pyspark中清理数据字段类型的功能

    Args:
        row_dict (Dict[str,Any]): str int float
        key_type_map (Dict[str,str]): s

    Returns:
        row_dict (Dict[str,Any]): s
    """
    for key in row_dict.keys():
        if key not in key_type_map:
            raise KeyError(
                f"{key} not in {json.dumps(key_type_map,ensure_ascii=False)}"
            )
        if key_type_map[key] == "str":
            if not isinstance(row_dict[key], str):
                row_dict[key] = ""
            row_dict[key] = conver_str(row_dict[key])
        elif key_type_map[key] == "int":
            if not isinstance(row_dict[key], int):
                row_dict[key] = 0
        elif key_type_map[key] == "float":
            if not isinstance(row_dict[key], float):
                row_dict[key] = 0.0
    return row_dict


def conver_str(origin_str: str) -> str:
    """conver_str

    用于往mysql写数据的时候的字符型数据的转换

    args:
        origin_str (str): 原始的字符型值

    returns:
        conver_str (str): 处理后的字符型值
    """
    return (
        origin_str.replace("\\", "\\\\")
        .replace("\b", "\\b")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
        .replace("\\x1A", "\\Z")
        .replace("\\x00", "\\0")
        .replace("'", "\\'")
        .replace('"', '\\"')
    )
