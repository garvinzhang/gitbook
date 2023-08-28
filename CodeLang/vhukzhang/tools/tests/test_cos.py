#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR)

from tools.tests.test_init import INIT_ALL, GetFastLog

test_log = GetFastLog(__file__)


def test_download():
    localFilePath = f"{DIR}/tmp/file/aaa.png"
    remoteCosPath = "url_crawl/wxmp_emu/aaa.png"
    ok, err = INIT_ALL.COS.DownloadFile(localFilePath, remoteCosPath)
    test_log.info(ok)
    test_log.info(err)


def test_upload():
    localFilePath = f"{DIR}/tmp/file/test_qlabel.csv"
    remoteCosPath = "url_crawl/wxmp_emu/test_qlabel.csv"
    ok, cosUrl, err = INIT_ALL.COS.UploadFile(localFilePath, remoteCosPath)
    test_log.info(ok)
    test_log.info(cosUrl)
    test_log.info(err)


# test_upload()
