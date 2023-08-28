#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from typing import NamedTuple, Tuple

from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../lib"))
sys.path.append(lib_path)

from base.utils import get_logger

logger = get_logger()


class CosConf(NamedTuple):
    bucketName: str
    bucketId: str
    secretKey: str
    secretId: str
    region: str


class CosUtils:
    """CosUtils

    Args:
        cos_conf (CosConf): sss

    Attributes:
        upload_file: 上传文件
        download_file: 下载文件
    """

    def __init__(self, cos_conf: CosConf) -> None:
        config = CosConfig(
            Region=cos_conf.region,
            SecretKey=cos_conf.secretKey,
            SecretId=cos_conf.secretId,
            Token=None,
            Scheme="https",
            Endpoint=f"cos-internal.{cos_conf.region}.tencentcos.cn",
            ServiceDomain="service.cos.tencentcos.cn",
        )
        self.client = CosS3Client(config)
        self.region = cos_conf.region
        self.bucket = cos_conf.bucketName + "-" + cos_conf.bucketId

    def upload_file(
        self,
        local_file_path: str,
        remote_cos_path: str,
    ) -> Tuple[str, str]:
        """upload_file

        Args:
            local_file_path (str): 本地文件路径
            remote_cos_path (str): COS远程文件路径

        Returns:
            cos_url (str): COS链接
            err (str): 失败信息
        """
        err = ""
        cos_url = (
            f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{remote_cos_path}"
        )
        for __ in range(0, 10):
            try:
                self.client.upload_file(
                    Bucket=self.bucket,
                    Key=remote_cos_path,
                    LocalFilePath=local_file_path,
                )
                err = ""
                break
            except CosClientError as ex:
                err = str(ex)
            except CosServiceError as ex:
                err = str(ex)
        return cos_url, err

    def download_file(
        self,
        local_file_path: str,
        remote_cos_path: str,
    ) -> str:
        """download_file

        Args:
            local_file_path (str): 本地文件路径
            remote_cos_path (str): COS远程文件路径

        Returns:
            ok (bool): 是否成功
            err (str): 失败信息
        """
        err = ""
        for __ in range(0, 10):
            try:
                self.client.download_file(
                    Bucket=self.bucket,
                    Key=remote_cos_path,
                    DestFilePath=local_file_path,
                )
                err = ""
                break
            except CosClientError as ex:
                err = str(ex)
            except CosServiceError as ex:
                err = str(ex)
        return err
