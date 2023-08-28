#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NamedTuple, List, Dict, Set


class Demo(NamedTuple):
    A: List
    B: Dict
    C: Set


class BoolErr(NamedTuple):
    ok: bool
    err: str


class RetErr(NamedTuple):
    ret: int
    err: str
