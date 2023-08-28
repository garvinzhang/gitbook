#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Tuple, NamedTuple

# TODO(vhukzhang): Change some
# FIXME(vhukzhang): safs
# NOTE(vhukzhang): asf

code: int = 10


class Point(NamedTuple):
    coord: Tuple[int, int] = (0, 0)
    label: str = ""


pointClass = Point()
pointClass.coord

raise FileNotFoundError("sad")

# 字符串不建议使用 += 的方式合并字符串，耗时、耗空间；建议使用列表 [] 保存字符串，循环结束后再 join 合并字符串。 ''.join([])

# 新版的异常处理方式 raise ValueError("message")

# 建议用异常替代函数的错误返回码 例如文件不存在可以用 raise FileNotExist()

# 在exception子句中，不能用 raise ex；而是直接raise就可以了。因为可以报错原始的traceback信息
# 或者 raise AnotherException(str(ex))

# raise MyException()

# __ 双下划线 表示不需要的变量！
