#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
from typing import Dict

from src_cal_score_trend import CalScoreTrend
from mysql import Mysql, MysqlConf
from util import UTIL

from pyspark.sql import SparkSession


SPARK = SparkSession.builder.enableHiveSupport().getOrCreate()
REPARTITION_NUM = 200
mysqlConf = MysqlConf(
    host="financial2.mdb.mig",
    user="writeuser",
    password="TLb@8yLHm5FE8k",
    port=24055,
)


def cleanType(row: Dict) -> Dict:
    if type(row["labels"]) is not str:
        row["labels"] = ""
    if type(row["score_trend"]) is not str:
        row["score_trend"] = ""
    if type(row["week_heat"]) is not int:
        row["week_heat"] = 0
    if type(row["week_heat_inc"]) is not int:
        row["week_heat_inc"] = 0
    if type(row["total_heat"]) is not int:
        row["total_heat"] = 0
    if type(row["week_heat_inc_ratio"]) is not float:
        row["week_heat_inc_ratio"] = 0.0
    return row


def handle(rows):
    mdbTableName = "report.company_risk_score"
    MYSQL = Mysql(mysqlConf=mysqlConf)
    rowDictList = []
    rowCnt = 0
    for row in rows:
        row_dict = row.asDict()
        row_dict = cleanType(row=row_dict)
        # 判断属于哪一种情况
        scoreTrendOri = row_dict["score_trend"]
        if row_dict["score_trend"]:  # 有趋势分，说明是趋势累加的正常情况
            status = 0
            score_trend = CalScoreTrend(
                status=status,
                score=row_dict["score"],
                scoreTrend=scoreTrendOri,
            )
            scoreMap = json.loads(scoreTrendOri)
            if scoreMap["score"][-1] != round(row_dict["score"], 1):
                status = 3  # 说明得分有波动
        else:  # 无趋势分，说明是新增的数据
            status = 1
            score_trend = CalScoreTrend(
                status=status,
                score=row_dict["score"],
                scoreTrend="",
            )
        row_dict["score_trend"] = score_trend
        row_dict["status"] = status
        row_dict["ds"] = UTIL.GetDs(1)
        # 插入或更新数据
        rowDictList.append(row_dict)
        rowCnt += 1
        if rowCnt == 10000:
            ok, res, commitErr = MYSQL.InsertDatasTrue(
                tableName=mdbTableName,
                datas=rowDictList,
                update=True,
            )
            if not ok:
                print(commitErr)
                for insertErr in res:
                    robotMsg = "InsertDataErr:" + json.dumps(insertErr)
                    print(robotMsg)
            rowDictList = []
            rowCnt = 0
    ok, res, commitErr = MYSQL.InsertDatasTrue(
        tableName=mdbTableName,
        datas=rowDictList,
        update=True,
    )
    if not ok:
        print(commitErr)
        for insertErr in res:
            robotMsg = "InsertDataErr:" + json.dumps(insertErr)
            print(robotMsg)
    rowDictList = []
    rowCnt = 0


def backScoreTrend():
    """backScoreTrend

    分数趋势回扫
    """
    mdbTableName = "report.company_risk_score"
    mdbSelectFields = "cid,score_trend,ds,status"
    dataMapList = []
    dataMap = {}
    old_ds = UTIL.GetDs(2)
    dataMap["ds"] = UTIL.GetDs(1)
    dataMap["status"] = 2

    sqlStr = f"SELECT {mdbSelectFields} FROM {mdbTableName} WHERE ds={old_ds}"
    MYSQL = Mysql(mysqlConf=mysqlConf)
    ok, datas, err = MYSQL.Select(sqlStr=sqlStr)
    if not ok:
        robotMsg = f"SelectDataError:{err}|sqlStr:{sqlStr}|datas:{datas}"
        print(robotMsg)
    print(f"回扫风险分数企业数:{len(datas)}")
    for data in datas:
        dataMap["cid"] = data[0]
        oldScoreTrend = data[1]
        dataMap["score_trend"] = CalScoreTrend(
            status=dataMap["status"],
            score=0,
            scoreTrend=oldScoreTrend,
        )
        dataMapList.append(dataMap)
    # 批量插入数据
    ok, res, commitErr = MYSQL.InsertDatasTrue(
        tableName=mdbTableName,
        datas=dataMapList,
        update=True,
    )
    if not ok:
        print(commitErr)
        for insertErr in res:
            robotMsg = "InsertDataErr:" + json.dumps(insertErr)
            print(robotMsg)


def main():
    ds = UTIL.GetDs(1)
    old_ds = UTIL.GetDs(2)
    tableName = "sh2_urlsafe.t_md_urlsafe_ngf_ui_company_risk_info"
    selectFields = "cid,company,labels,score,internet_score,commerce_score,business_score,relation_score,judicial_score,sentiment_score,week_heat,week_heat_inc,week_heat_inc_ratio,total_heat"
    hqlStr = f"""
    SELECT A.cid,A.company,A.labels,A.score,A.commerce_score,A.business_score,A.relation_score,A.judicial_score,A.sentiment_score,A.week_heat,A.week_heat_inc,A.week_heat_inc_ratio,A.total_heat,B.score_trend FROM 
    (SELECT {selectFields} FROM {tableName} WHERE ds={ds} AND score>0.1)A
    LEFT JOIN 
    (SELECT cid,score_trend FROM sh2_urlsafe.t_td_urlsafe_company_risk_score_trend WHERE ds={old_ds})B
    ON A.cid=B.cid
    """
    df = SPARK.sql(hqlStr)
    df.show()
    startTime = time.time()
    df.repartition(REPARTITION_NUM).rdd.foreachPartition(handle)
    endTime = time.time()
    useTime = round(endTime - startTime, 3)
    print("partitionUseTime:", str(useTime))
    SPARK.stop()

    # 回扫风险分数企业
    startTime = time.time()
    backScoreTrend()
    endTime = time.time()
    useTime = round(endTime - startTime, 3)
    print("backUpdateUseTime:", str(useTime))


if __name__ == "__main__":
    startTime = time.time()
    main()
    endTime = time.time()
    useTime = round(endTime - startTime, 3)
    print("useTime:" + str(useTime))
