import sys
import time
from typing import Dict

from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession
from elasticsearch.helpers import bulk


SPARK = SparkSession.builder.enableHiveSupport().getOrCreate()
SPARK.sql("set hive.exec.dynamic.partition.mode = nonstrict")
SPARK.sql("set hive.exec.dynamic.partition=true")
ES_CONF = {
    "host": "http://10.101.198.88:9200",
    "auth": "elastic",
    "pwd": "Urlsec_goods",
    "index": "gs_company_2_8",
}
REPARTITION_NUM = 200
# LIMIT = "LIMIT 1000000"
LIMIT = ""


def cleanType(rowDict: Dict) -> Dict:
    baseTime = "1970-01-01 00:00:00"
    if type(rowDict["id"]) is not int:
        rowDict["id"] = 0
    if type(rowDict["cid"]) is not int:
        rowDict["cid"] = 0
    if type(rowDict["base"]) is not str:
        rowDict["base"] = ""
    if type(rowDict["name"]) is not str:
        rowDict["name"] = ""
    rowDict["name_"] = rowDict["name"]
    if type(rowDict["name_en"]) is not str:
        rowDict["name_en"] = ""
    if type(rowDict["name_alias"]) is not str:
        rowDict["name_alias"] = ""
    if type(rowDict["history_names"]) is not str:
        rowDict["history_names"] = ""
    if type(rowDict["legal_entity_id"]) is not int:
        rowDict["legal_entity_id"] = 0
    if type(rowDict["legal_entity_type"]) is not int:
        rowDict["legal_entity_type"] = 0
    if type(rowDict["reg_number"]) is not str:
        rowDict["reg_number"] = ""
    if type(rowDict["company_org_type"]) is not str:
        rowDict["company_org_type"] = "-"
    if not rowDict["company_org_type"]:
        rowDict["company_org_type"] = "-"
    if type(rowDict["reg_location"]) is not str:
        rowDict["reg_location"] = ""
    if type(rowDict["estiblish_time"]) is not str:
        rowDict["estiblish_time"] = baseTime
    rowDict["estiblish_time"] = rowDict["estiblish_time"].split(".")[0]
    if type(rowDict["from_time"]) is not str:
        rowDict["from_time"] = baseTime
    rowDict["from_time"] = rowDict["from_time"].split(".")[0]
    if type(rowDict["to_time"]) is not str:
        rowDict["to_time"] = baseTime
    rowDict["to_time"] = rowDict["to_time"].split(".")[0]
    if type(rowDict["business_scope"]) is not str:
        rowDict["business_scope"] = ""
    if type(rowDict["reg_institute"]) is not str:
        rowDict["reg_institute"] = ""
    if type(rowDict["approved_time"]) is not str:
        rowDict["approved_time"] = baseTime
    rowDict["approved_time"] = rowDict["approved_time"].split(".")[0]
    if type(rowDict["reg_status"]) is not str:
        rowDict["reg_status"] = ""
    if type(rowDict["reg_capital"]) is not str:
        rowDict["reg_capital"] = ""
    if type(rowDict["org_number"]) is not str:
        rowDict["org_number"] = ""
    if type(rowDict["org_approved_institute"]) is not str:
        rowDict["org_approved_institute"] = ""
    if type(rowDict["current_cid"]) is not int:
        rowDict["current_cid"] = 0
    if type(rowDict["parent_cid"]) is not int:
        rowDict["parent_cid"] = 0
    if type(rowDict["company_type"]) is not int:
        rowDict["company_type"] = 0
    if type(rowDict["credit_code"]) is not str:
        rowDict["credit_code"] = ""
    if type(rowDict["score"]) is not str:
        rowDict["score"] = ""
    if type(rowDict["category_code"]) is not str:
        rowDict["category_code"] = ""
    if type(rowDict["lat"]) is not str:
        rowDict["lat"] = 0.0
    rowDict["lat"] = float(rowDict["lat"])
    if type(rowDict["lng"]) is not str:
        rowDict["lng"] = 0.0
    rowDict["lng"] = float(rowDict["lng"])
    if type(rowDict["area_code"]) is not int:
        rowDict["area_code"] = "0"
    rowDict["area_code"] = str(rowDict["area_code"])
    if type(rowDict["reg_capital_amount"]) is not int:
        rowDict["reg_capital_amount"] = 0
    if type(rowDict["reg_capital_currency"]) is not str:
        rowDict["reg_capital_currency"] = ""
    if type(rowDict["actual_capital_amount"]) is not int:
        rowDict["actual_capital_amount"] = 0
    if type(rowDict["actual_capital_currency"]) is not str:
        rowDict["actual_capital_currency"] = ""
    if type(rowDict["reg_status_std"]) is not str:
        rowDict["reg_status_std"] = ""
    if type(rowDict["social_security_staff_num"]) is not int:
        rowDict["social_security_staff_num"] = 0
    if type(rowDict["cancel_date"]) is not str:
        rowDict["cancel_date"] = baseTime
    rowDict["cancel_date"] = rowDict["cancel_date"].split(".")[0]
    if type(rowDict["cancel_reason"]) is not str:
        rowDict["cancel_reason"] = ""
    if type(rowDict["revoke_date"]) is not str:
        rowDict["revoke_date"] = baseTime
    rowDict["revoke_date"] = rowDict["revoke_date"].split(".")[0]
    if type(rowDict["revoke_reason"]) is not str:
        rowDict["revoke_reason"] = ""
    if type(rowDict["emails"]) is not str:
        rowDict["emails"] = ""
    rowDict["emails"] = rowDict["emails"].replace(",;,", ",")[:-1]
    if type(rowDict["phones"]) is not str:
        rowDict["phones"] = ""
    rowDict["phones"] = rowDict["phones"].replace(",;,", ",")[:-1]
    if type(rowDict["wechat_public_num"]) is not str:
        rowDict["wechat_public_num"] = ""
    if type(rowDict["logo"]) is not str:
        rowDict["logo"] = ""
    if type(rowDict["crawled_time"]) is not str:
        rowDict["crawled_time"] = baseTime
    rowDict["crawled_time"] = rowDict["crawled_time"].split(".")[0]
    if type(rowDict["create_time"]) is not str:
        rowDict["create_time"] = baseTime
    rowDict["create_time"] = rowDict["create_time"].split(".")[0]
    if type(rowDict["update_time"]) is not str:
        rowDict["update_time"] = baseTime
    rowDict["update_time"] = rowDict["update_time"].split(".")[0]
    if type(rowDict["deleted"]) is not int:
        rowDict["deleted"] = 0
    if type(rowDict["class_ids"]) is not str:
        rowDict["class_ids"] = ""
    rowDict["class_ids_is_null"] = 0
    if rowDict["class_ids"]:
        rowDict["class_ids_is_null"] = 1
    if type(rowDict["class_names"]) is not str:
        rowDict["class_names"] = ""
    if type(rowDict["province"]) is not str:
        rowDict["province"] = ""
    if type(rowDict["city"]) is not str:
        rowDict["city"] = ""
    if type(rowDict["zone"]) is not str:
        rowDict["zone"] = ""
    if type(rowDict["labels"]) is not str:
        rowDict["labels"] = ""
    if type(rowDict["sum_score"]) is not float:
        rowDict["sum_score"] = 0.0
    if type(rowDict["internet_score"]) is not float:
        rowDict["internet_score"] = 0.0
    if type(rowDict["commerce_score"]) is not float:
        rowDict["commerce_score"] = 0.0
    if type(rowDict["business_score"]) is not float:
        rowDict["business_score"] = 0.0
    if type(rowDict["relation_score"]) is not float:
        rowDict["relation_score"] = 0.0
    if type(rowDict["judicial_score"]) is not float:
        rowDict["judicial_score"] = 0.0
    if type(rowDict["sentiment_score"]) is not float:
        rowDict["sentiment_score"] = 0.0
    if type(rowDict["week_heat"]) is not int:
        rowDict["week_heat"] = 0
    if type(rowDict["week_heat_inc"]) is not int:
        rowDict["week_heat_inc"] = 0
    if type(rowDict["week_heat_inc_ratio"]) is not float:
        rowDict["week_heat_inc_ratio"] = 0.0
    if type(rowDict["total_heat"]) is not int:
        rowDict["total_heat"] = 0
    if type(rowDict["category_name"]) is not str:
        rowDict["category_name"] = "-"
    if not rowDict["category_name"]:
        rowDict["category_name"] = "-"
    if type(rowDict["company_labels"]) is not str:
        rowDict["company_labels"] = "-"
    if not rowDict["company_labels"]:
        rowDict["company_labels"] = "-"
    if type(rowDict["category_name_second"]) is not str:
        rowDict["category_name_second"] = ""
    if type(rowDict["category_name_third"]) is not str:
        rowDict["category_name_third"] = ""
    if type(rowDict["legal_entity"]) is not str:
        rowDict["legal_entity"] = ""
    if type(rowDict["platform_cnt"]) is not int:
        rowDict["platform_cnt"] = 0
    if type(rowDict["ad_cnt"]) is not int:
        rowDict["ad_cnt"] = 0
    if type(rowDict["wx_account_cnt"]) is not int:
        rowDict["wx_account_cnt"] = 0
    if type(rowDict["wx_article_cnt"]) is not int:
        rowDict["wx_article_cnt"] = 0
    return rowDict


def handle(rows):
    ES = Elasticsearch(
        [ES_CONF["host"]],
        http_auth=(ES_CONF["auth"], ES_CONF["pwd"]),
        sniff_on_start=False,
        sniff_on_connection_fail=False,
        sniffer_timeout=None,
    )
    num = 0
    docs = []
    for row in rows:
        rowDict = row.asDict()
        rowDict = cleanType(rowDict=rowDict)
        num += 1
        doc = {"delete": {"_index": ES_CONF["index"], "_id": rowDict["id"]}}
        docs.append(doc)

        # 使用bulk API批量删除数据
        if num % 1000 == 0:
            ES.bulk(index=ES_CONF["index"], body=docs)  # type: ignore
            docs = []
            num = 0
    # 最后剩下的没插入的
    if num != 0:
        ES.bulk(index=ES_CONF["index"], body=docs)  # type: ignore


def main():
    print("start")
    ds = sys.argv[1]
    tableName = "sh2_urlsafe.t_fd_urlsafe_ngf_company_wide_table_dec"
    selectFields = """id,cid,base,name,name_en,name_alias,history_names,legal_entity_id,legal_entity_type,reg_number,company_org_type,
                    reg_location,estiblish_time,from_time,to_time,business_scope,reg_institute,approved_time,reg_status,reg_capital,
                    org_number,org_approved_institute,current_cid,parent_cid,company_type,credit_code,score,category_code,lat,lng,
                    area_code,reg_capital_amount,reg_capital_currency,actual_capital_amount,actual_capital_currency,reg_status_std,
                    social_security_staff_num,cancel_date,cancel_reason,revoke_date,revoke_reason,emails,phones,wechat_public_num,
                    logo,crawled_time,create_time,update_time,deleted,class_ids,class_names,province,city,zone,labels,sum_score,
                    internet_score,commerce_score,business_score,relation_score,judicial_score,sentiment_score,week_heat,week_heat_inc,
                    week_heat_inc_ratio,total_heat,category_name,company_labels,category_name_second,category_name_third,legal_entity,
                    platform_cnt,ad_cnt,wx_account_cnt,wx_article_cnt"""
    hqlStr = f"SELECT {selectFields} FROM {tableName} WHERE ds={ds} {LIMIT}"
    df = SPARK.sql(hqlStr)
    df.show(10)
    startTime = time.time()
    df.repartition(REPARTITION_NUM).rdd.foreachPartition(handle)
    endTime = time.time()
    useTime = round(endTime - startTime, 3)
    print("handleUseTime:" + str(useTime))
    SPARK.stop()
    print("stop")


if __name__ == "__main__":
    startTime = time.time()
    main()
    endTime = time.time()
    useTime = round(endTime - startTime, 3)
    print("mainUseTime:" + str(useTime))
