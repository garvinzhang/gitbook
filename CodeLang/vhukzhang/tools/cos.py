#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Tuple, NamedTuple

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError


class CosConf(NamedTuple):
    """CosConf

    cos 连接所需的参数
    """

    bucketName: str
    bucketId: str
    secretKey: str
    secretId: str
    region: str = "ap-guangzhou"


class Cos(object):
    """FastCos

    Args:
        cosConf (CosConf): sss

    Attributes:
        UploadFile: 上传文件
        DownloadFile: 下载文件
    """

    def __init__(self, cosConf: CosConf) -> None:
        config = CosConfig(
            Region=cosConf.region,
            SecretKey=cosConf.secretKey,
            SecretId=cosConf.secretId,
            Token=None,
            Scheme="https",
            Endpoint=f"cos-internal.{cosConf.region}.tencentcos.cn",
            ServiceDomain="service.cos.tencentcos.cn",
        )
        self.client = CosS3Client(config)
        self.region = cosConf.region
        self.bucket = cosConf.bucketName + "-" + cosConf.bucketId

    def UploadFile(
        self,
        localFilePath: str,
        remoteCosPath: str,
    ) -> Tuple[bool, str, str]:
        """UploadFile

        Args:
            localFilePath (str): 本地文件路径
            remoteCosPath (str): COS远程文件路径

        Returns:
            ok (bool): 是否成功
            cosUrl (str): COS链接
            err (str): 失败信息
        """
        ok = False
        err = ""
        cosUrl = f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{remoteCosPath}"
        for _ in range(0, 10):
            try:
                _ = self.client.upload_file(
                    Bucket=self.bucket,
                    Key=remoteCosPath,
                    LocalFilePath=localFilePath,
                )
                ok = True
                break
            except CosClientError or CosServiceError as ex:
                print(ex)
                err = str(ex)
        return ok, cosUrl, err

    def DownloadFile(
        self,
        localFilePath: str,
        remoteCosPath: str,
    ) -> Tuple[bool, str]:
        """DownloadFile

        Args:
            localFilePath (str): 本地文件路径
            remoteCosPath (str): COS远程文件路径

        Returns:
            ok (bool): 是否成功
            err (str): 失败信息
        """
        ok = False
        err = ""
        for _ in range(0, 10):
            try:
                _ = self.client.download_file(
                    Bucket=self.bucket,
                    Key=remoteCosPath,
                    DestFilePath=localFilePath,
                )
                ok = True
                break
            except CosClientError or CosServiceError as ex:
                print(ex)
                err = str(ex)
        return ok, err
