#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
from typing import Dict
from datetime import datetime, date, timedelta

from pyspark.sql import SparkSession, Row


class Util(object):
    def GetNowtime(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def GetDate(self, backDay: int = 0) -> str:
        return (date.today() - timedelta(backDay)).strftime("%Y-%m-%d")

    def GetDs(self, backDay: int = 0) -> int:
        return int((date.today() - timedelta(backDay)).strftime("%Y%m%d"))


UTIL = Util()
SPARK = SparkSession.builder.enableHiveSupport().getOrCreate()
SPARK.sql("set hive.exec.dynamic.partition.mode = nonstrict")
SPARK.sql("set hive.exec.dynamic.partition=true")
REPARTITION_NUM = 200
TMP_TABLE = "tmp_hive_table"
ds1 = sys.argv[1]  # %YYYYMMDD%
ds2 = sys.argv[2]  # %LASTDAY%
str_ds = ds1[:4] + "-" + ds1[4:6] + "-" + ds1[6:]
ds_list = [(date.today() - timedelta(i + 1)).strftime("%Y-%m-%d") for i in range(7)]
backDayEnd = ds_list.index(str_ds)
backDayStart = backDayEnd + 93  # len=93
trendDateList = [
    UTIL.GetDate(backDay) for backDay in range(backDayStart, backDayEnd, -1)
]


def cleanType(row_dict: Dict) -> Dict:
    if type(row_dict["labels"]) is not str:
        row_dict["labels"] = ""
    if type(row_dict["score_trend"]) is not str:
        row_dict["score_trend"] = ""
    if type(row_dict["date_ds"]) is not int:
        row_dict["date_ds"] = 0
    if type(row_dict["week_heat"]) is not int:
        row_dict["week_heat"] = 0
    if type(row_dict["week_heat_inc"]) is not int:
        row_dict["week_heat_inc"] = 0
    if type(row_dict["total_heat"]) is not int:
        row_dict["total_heat"] = 0
    if type(row_dict["week_heat_inc_ratio"]) is not float:
        row_dict["week_heat_inc_ratio"] = 0.0
    row_dict["week_heat_inc_ratio"] = round(row_dict["week_heat_inc_ratio"], 2)
    if type(row_dict["score"]) is not float:
        row_dict["score"] = 0.0
    row_dict["score"] = round(row_dict["score"], 1)
    if type(row_dict["internet_score"]) is not float:
        row_dict["internet_score"] = 0.0
    row_dict["internet_score"] = round(row_dict["internet_score"], 3)
    if type(row_dict["commerce_score"]) is not float:
        row_dict["commerce_score"] = 0.0
    row_dict["commerce_score"] = round(row_dict["commerce_score"], 3)
    if type(row_dict["business_score"]) is not float:
        row_dict["business_score"] = 0.0
    row_dict["business_score"] = round(row_dict["business_score"], 3)
    if type(row_dict["relation_score"]) is not float:
        row_dict["relation_score"] = 0.0
    row_dict["relation_score"] = round(row_dict["relation_score"], 3)
    if type(row_dict["judicial_score"]) is not float:
        row_dict["judicial_score"] = 0.0
    row_dict["judicial_score"] = round(row_dict["judicial_score"], 3)
    if type(row_dict["sentiment_score"]) is not float:
        row_dict["sentiment_score"] = 0.0
    row_dict["sentiment_score"] = round(row_dict["sentiment_score"], 3)
    return row_dict


def handle(rows):
    for row in rows:
        row_dict = row.asDict()
        row_dict = cleanType(row_dict=row_dict)

        # 判断属于哪一种情况
        if row_dict["date_ds"] == 0:  # 说明是新增的数据
            status = 1
            trendScoreList = [row_dict["score"] for __ in range(93)]
            dstScoreMap = {
                "date": trendDateList,
                "score": trendScoreList,
            }
        else:  # 说明是旧的正常数据
            if row_dict["score"] < 0.1:  # 说明今天没分数，要沿用昨天的
                status = 2
                oriScoreMap = json.loads(row_dict["score_trend"])
                del oriScoreMap["date"][0]
                del oriScoreMap["score"][0]
                oriScoreMap["date"].append(oriScoreMap["date"][-1])
                oriScoreMap["score"].append(oriScoreMap["score"][-1])
                dstScoreMap = oriScoreMap
            else:  # 正常的情况，新增新一天的分数
                status = 0
                oriScoreMap = json.loads(row_dict["score_trend"])
                del oriScoreMap["date"][0]
                del oriScoreMap["score"][0]
                # 分数是否有波动
                if oriScoreMap["score"][-1] != row_dict["score"]:
                    status = 3
                oriScoreMap["date"].append(str_ds)
                oriScoreMap["score"].append(row_dict["score"])
                dstScoreMap = oriScoreMap
        row_dict["date_ds"] = int(ds1)
        row_dict["status"] = status
        row_dict["score_trend"] = json.dumps(dstScoreMap)
        result = Row(**row_dict)
        yield result


def main():
    srcTableName = "sh2_urlsafe.t_md_urlsafe_ngf_ui_company_risk_info"
    dstTableName = "sh2_urlsafe.t_td_urlsafe_company_risk_score_trend"
    selectFields = "cid,company,labels,score,internet_score,commerce_score,business_score,relation_score,judicial_score,sentiment_score,week_heat,week_heat_inc,week_heat_inc_ratio,total_heat"
    # 踩坑 写入字段的顺序要和HIVE表一致
    # insertFields = "cid,company,labels,score,internet_score,commerce_score,business_score,relation_score,judicial_score,sentiment_score,week_heat,week_heat_inc,week_heat_inc_ratio,total_heat,score_trend,status,date_ds"
    insertFields = "cid,company,labels,score,internet_score,commerce_score,business_score,relation_score,judicial_score,sentiment_score,score_trend,status,week_heat,week_heat_inc,week_heat_inc_ratio,total_heat,date_ds"

    hqlStr = f"""
    SELECT A.cid,A.company,A.labels,A.score,A.internet_score,A.commerce_score,A.business_score,A.relation_score,A.judicial_score,A.sentiment_score,A.week_heat,A.week_heat_inc,A.week_heat_inc_ratio,A.total_heat,B.score_trend,B.date_ds FROM 
    (SELECT {selectFields} FROM {srcTableName} WHERE ds={ds1} AND score>0.1)A
    LEFT JOIN 
    (SELECT cid,score_trend,date_ds FROM {dstTableName} WHERE ds={ds2})B
    ON A.cid=B.cid
    """

    df = SPARK.sql(hqlStr)
    df.show(10)
    startTime = time.time()
    res_rdd = df.repartition(REPARTITION_NUM).rdd.mapPartitions(handle)
    endTime = time.time()
    useTime = round(endTime - startTime, 3)
    print("handleUseTime:" + str(useTime))
    res_df = res_rdd.toDF()
    res_df.show(10)
    res_df.createOrReplaceTempView(TMP_TABLE)
    SPARK.sql(
        f"INSERT OVERWRITE TABLE {dstTableName} PARTITION(ds={ds1}) SELECT {insertFields} FROM {TMP_TABLE}"
        # f"INSERT INTO TABLE {dstTableName} PARTITION(ds={ds1}) SELECT {insertFields} FROM {TMP_TABLE}"
    )
    SPARK.stop()


if __name__ == "__main__":
    startTime = time.time()
    main()
    endTime = time.time()
    useTime = round(endTime - startTime, 3)
    print("mainUseTime:" + str(useTime))
