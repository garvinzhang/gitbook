#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class FastLog(object):
    """FastLog

    方便的日志模块

    Args:
        None

    Attributes:
        GetLogger: 日志模块，默认输出到控制台和日志文件中
        GetLogstr: 输出日志字符串，使用场景是企业微信机器人告警等服务
    """

    def __init__(self) -> None:
        pass

    def GetLogger(
        self,
        fileName: str,
        level: str = "info",
        screenStream: bool = True,
        backupCount: int = 1,
    ) -> logging.Logger:
        """get_logger

        Args:
            filename (str): 日志保存文件路径
            level (str="info"): 日志等级
            screenStream (bool=True): 是否输出到控制台
            backupCount (int=1): 日志保存的天数

        Returns:
            logger (logging.Logger): 日志模块
        """
        logger = logging.getLogger(fileName)

        formatter = logging.Formatter(
            "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        if level == "debug":
            logger.setLevel(logging.DEBUG)
        elif level == "info":
            logger.setLevel(logging.INFO)
        elif level == "warning":
            logger.setLevel(logging.WARNING)
        elif level == "error":
            logger.setLevel(logging.ERROR)
        elif level == "critical":
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(logging.INFO)

        if screenStream:
            log_screen = logging.StreamHandler()
            log_screen.setFormatter(formatter)
            logger.addHandler(log_screen)

        file_handler = TimedRotatingFileHandler(
            filename=fileName,
            when="MIDNIGHT",
            interval=1,
            backupCount=backupCount,
        )
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    def GetLogStr(
        self,
        fileName: str,
        fileLine: int,
        msg: str,
    ) -> str:
        """get_logstr

        Args:
            fileName (str): 日志文件名字__file__
            fileLine (int): 当前行数 sys._getframe().f_lineno
            msg (str): 日志信息

        Returns:
            logstr (str): 标准化日志字符串
        """
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logStr = f"{now_time}|{fileName}:{fileLine}|{msg}"
        return logStr
