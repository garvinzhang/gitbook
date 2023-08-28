import json
import os
import sys
import time
import uuid

import jwt
import requests

DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

sys.path.append(DIR)
from tools.fast_log import FastLog
from tools.rainbow import RAINBOW

RAINBOW.Init()
FAST_LOG = FastLog()
model_log = FAST_LOG.GetLogger(fileName=f"{DIR}/tmp/log/model_qlabel.log")


class Qlabel:
    def __init__(self) -> None:
        self.api = "http://qlabel.woa.com/openapi/dataset/"
        qlabelConf = RAINBOW.GetValue("qlabel")
        self.iss = qlabelConf["iss"]
        self.key = qlabelConf["key"]
        self.algorithm = qlabelConf["algorithm"]
        self.nonce = str(uuid.uuid4()).replace("-", "")
        self.iat = int(round(time.time() * 1000))

    def generateSign(self) -> str:
        payload = {
            "iss": self.iss,
            "iat": self.iat,
            "nonce": self.nonce,
        }
        headers = {"alg": self.algorithm}
        sign = jwt.encode(
            payload,
            key=self.key,
            algorithm=self.algorithm,
            headers=headers,
        )
        return sign

    # 上传成功 需要创建动态任务
    def submitImportTask(
        self,
        projectId: int,
        cosUrl: str,
        formalCode: str,
        action: str = "submitImportTask",
    ):
        sign = self.generateSign()
        headers = {"content-type": "application/json", "Authorization": sign}
        url = self.api + action
        s = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": "1",
                "method": action,
                "params": {
                    "project_id": projectId,
                    "url": cosUrl,
                    "formal_code": formalCode,
                },
            }
        )
        r = requests.post(url, data=s, headers=headers)
        model_log.info(r.status_code)
        print(r.text)

    def exportData(self, projectId: int, action: str = "exportDatasetTasks"):
        sign = self.generateSign()
        headers = {"content-type": "application/json", "Authorization": sign}
        url = self.api + action
        s = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": "1",
                "method": action,
                "params": {
                    "project_id": projectId,
                    "page": {"start": 0, "size": 50000, "returnTotal": 50000},
                },
            }
        )
        res = requests.post(url, data=s, headers=headers)
        model_log.debug(res.status_code)
        model_log.debug(res.text)
        label_result = json.loads(res.text)["result"]["data"]
        result_cnt = len(label_result)
        model_log.info(result_cnt)
        for lres in label_result:
            content = json.loads(lres["dataset_item_content"])["content"]
            model_log.debug(res)
            model_log.debug(type(res))
            model_log.debug(content)
            detail_status = lres["detail_status"]
            detail_is_valid = lres["detail_is_valid"]
            detail_label = lres["detail_label"]
            if detail_status == 30 and detail_is_valid == 1:
                verifyLabel = json.loads(detail_label)["tags"][0]["value"]
                model_log.info(verifyLabel)


QLABEL = Qlabel()
# QLABEL.exportData()
# QLABEL.submitImportTask()

"""
流程：
    从数据表中拉取需要审核的数据 -》 
    存成csv文件的格式 -》 
    将csv文件上传到COS -》 
    用接口发布到qlabel任务 -》 
    联系合作伙伴进行标注 -》 
    标注完成后，用接口导出并查看数据 -》 
    分析数据标注的质量，优化模型 -》 
    有效数据导入业务系统表
"""
