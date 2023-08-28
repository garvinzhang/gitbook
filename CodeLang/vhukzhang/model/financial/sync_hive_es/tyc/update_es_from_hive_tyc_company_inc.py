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
    "index": "gs_company_1_3",
}
REPARTITION_NUM = 10
#LIMIT = "LIMIT 100000"
LIMIT = ""


def cleanType(rowDict: Dict) -> Dict:
    base_time = "1970-01-01 00:00:00"
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
        rowDict["estiblish_time"] = base_time
    rowDict["estiblish_time"] = rowDict["estiblish_time"].split(".")[0]
    if type(rowDict["from_time"]) is not str:
        rowDict["from_time"] = base_time
    rowDict["from_time"] = rowDict["from_time"].split(".")[0]
    if type(rowDict["to_time"]) is not str:
        rowDict["to_time"] = base_time
    rowDict["to_time"] = rowDict["to_time"].split(".")[0]
    if type(rowDict["business_scope"]) is not str:
        rowDict["business_scope"] = ""
    if type(rowDict["reg_institute"]) is not str:
        rowDict["reg_institute"] = ""
    if type(rowDict["approved_time"]) is not str:
        rowDict["approved_time"] = base_time
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
        rowDict["cancel_date"] = base_time
    rowDict["cancel_date"] = rowDict["cancel_date"].split(".")[0]
    if type(rowDict["cancel_reason"]) is not str:
        rowDict["cancel_reason"] = ""
    if type(rowDict["revoke_date"]) is not str:
        rowDict["revoke_date"] = base_time
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
        rowDict["crawled_time"] = base_time
    rowDict["crawled_time"] = rowDict["crawled_time"].split(".")[0]
    if type(rowDict["create_time"]) is not str:
        rowDict["create_time"] = base_time
    rowDict["create_time"] = rowDict["create_time"].split(".")[0]
    if type(rowDict["update_time"]) is not str:
        rowDict["update_time"] = base_time
    rowDict["update_time"] = rowDict["update_time"].split(".")[0]
    if type(rowDict["deleted"]) is not int:
        rowDict["deleted"] = 0
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
        doc = {"_index": ES_CONF["index"], "_id": rowDict["id"], "_source": rowDict}
        docs.append(doc)

        # 使用bulk API批量插入数据
        if num % 1000 == 0:
            bulk(ES, docs)
            docs = []
            num = 0
    # 最后剩下的没插入的
    if num != 0:
        bulk(ES, docs)


def main():
    print("start")
    ds = sys.argv[1]
    tableName = "sh2_urlsafe.t_td_urlsafe_new_qiye_company_inc"
    selectFields = "id,cid,base,name,name_en,name_alias,history_names,legal_entity_id,legal_entity_type,reg_number,company_org_type,reg_location,estiblish_time,from_time,to_time,business_scope,reg_institute,approved_time,reg_status,reg_capital,org_number,org_approved_institute,current_cid,parent_cid,company_type,credit_code,score,category_code,lat,lng,area_code,reg_capital_amount,reg_capital_currency,actual_capital_amount,actual_capital_currency,reg_status_std,social_security_staff_num,cancel_date,cancel_reason,revoke_date,revoke_reason,emails,phones,wechat_public_num,logo,crawled_time,create_time,update_time,deleted"
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


main()