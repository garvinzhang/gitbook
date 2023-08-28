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
    "index": "sz_ads_1_0",
}
REPARTITION_NUM = 200
# LIMIT = "LIMIT 1000000"
LIMIT = ""


def cleanType(rowDict: Dict) -> Dict:
    base_time = "1970-01-01 00:00:00"
    if type(rowDict["id"]) is not int:
        rowDict["id"] = 0
    if type(rowDict["ad_global_id"]) is not int:
        rowDict["ad_global_id"] = 0
    if type(rowDict["ad_signature"]) is not str:
        rowDict["ad_signature"] = ""
    if type(rowDict["ad_obj_type"]) is not str:
        rowDict["ad_obj_type"] = ""
    if type(rowDict["ad_obj_key"]) is not str:
        rowDict["ad_obj_key"] = ""
    if type(rowDict["ad_obj_name"]) is not str:
        rowDict["ad_obj_name"] = ""
    if type(rowDict["ad_name"]) is not str:
        rowDict["ad_name"] = ""
    if type(rowDict["ad_text"]) is not str:
        rowDict["ad_text"] = ""
    if type(rowDict["ad_pic"]) is not str:
        rowDict["ad_pic"] = ""
    if type(rowDict["ad_pics_cos"]) is not str:
        rowDict["ad_pics_cos"] = ""
    if type(rowDict["ad_vedio"]) is not str:
        rowDict["ad_vedio"] = ""
    if type(rowDict["ad_vedios_cos"]) is not str:
        rowDict["ad_vedios_cos"] = ""
    if type(rowDict["ad_appear_url"]) is not str:
        rowDict["ad_appear_url"] = ""
    if type(rowDict["ad_appear_site"]) is not str:
        rowDict["ad_appear_site"] = ""
    if type(rowDict["ad_appear_domain"]) is not str:
        rowDict["ad_appear_domain"] = ""
    if type(rowDict["ad_appear_url_title"]) is not str:
        rowDict["ad_appear_url_title"] = ""
    if type(rowDict["ad_appear_url_snapshot"]) is not str:
        rowDict["ad_appear_url_snapshot"] = ""
    if type(rowDict["ad_click_url"]) is not str:
        rowDict["ad_click_url"] = ""
    if type(rowDict["ad_click_site"]) is not str:
        rowDict["ad_click_site"] = ""
    if type(rowDict["ad_click_domain"]) is not str:
        rowDict["ad_click_domain"] = ""
    if type(rowDict["ad_land_url"]) is not str:
        rowDict["ad_land_url"] = ""
    if type(rowDict["ad_land_site"]) is not str:
        rowDict["ad_land_site"] = ""
    if type(rowDict["ad_land_domain"]) is not str:
        rowDict["ad_land_domain"] = ""
    if type(rowDict["ad_land_url_title"]) is not str:
        rowDict["ad_land_url_title"] = ""
    if type(rowDict["ad_land_url_body"]) is not str:
        rowDict["ad_land_url_body"] = ""
    if type(rowDict["ad_land_url_snapshot"]) is not str:
        rowDict["ad_land_url_snapshot"] = ""
    if type(rowDict["publish_company"]) is not str:
        rowDict["publish_company"] = ""
    if type(rowDict["publish_icp_type"]) is not str:
        rowDict["publish_icp_type"] = ""
    if type(rowDict["publish_icp_num"]) is not str:
        rowDict["publish_icp_num"] = ""
    if type(rowDict["publish_province"]) is not str:
        rowDict["publish_province"] = ""
    if type(rowDict["publish_city"]) is not str:
        rowDict["publish_city"] = ""
    if type(rowDict["publish_area"]) is not str:
        rowDict["publish_area"] = ""
    if type(rowDict["publish_address"]) is not str:
        rowDict["publish_address"] = ""
    if type(rowDict["ad_agent"]) is not str:
        rowDict["ad_agent"] = ""
    if type(rowDict["ad_company"]) is not str:
        rowDict["ad_company"] = ""
    if type(rowDict["ad_icp_type"]) is not str:
        rowDict["ad_icp_type"] = ""
    if type(rowDict["ad_icp_num"]) is not str:
        rowDict["ad_icp_num"] = ""
    if type(rowDict["ad_province"]) is not str:
        rowDict["ad_province"] = ""
    if type(rowDict["ad_city"]) is not str:
        rowDict["ad_city"] = ""
    if type(rowDict["ad_area"]) is not str:
        rowDict["ad_area"] = ""
    if type(rowDict["ad_address"]) is not str:
        rowDict["ad_address"] = ""
    if type(rowDict["detect_ad_type"]) is not str:
        rowDict["detect_ad_type"] = ""
    if type(rowDict["detect_sub_type"]) is not str:
        rowDict["detect_sub_type"] = ""
    if type(rowDict["detect_result"]) is not int:
        rowDict["detect_result"] = 0
    if type(rowDict["detect_keywords"]) is not str:
        rowDict["detect_keywords"] = ""
    if type(rowDict["detect_reason"]) is not str:
        rowDict["detect_reason"] = ""
    if type(rowDict["detect_law_code"]) is not str:
        rowDict["detect_law_code"] = ""
    if type(rowDict["detect_law_src"]) is not str:
        rowDict["detect_law_src"] = ""
    if type(rowDict["detect_law_label"]) is not str:
        rowDict["detect_law_label"] = ""
    if type(rowDict["detect_law_detail"]) is not str:
        rowDict["detect_law_detail"] = ""
    if type(rowDict["crawler_ip"]) is not str:
        rowDict["crawler_ip"] = ""
    if type(rowDict["crawler_country"]) is not str:
        rowDict["crawler_country"] = ""
    if type(rowDict["crawler_province"]) is not str:
        rowDict["crawler_province"] = ""
    if type(rowDict["crawler_city"]) is not str:
        rowDict["crawler_city"] = ""
    if type(rowDict["insert_time"]) is not str:
        rowDict["insert_time"] = base_time
    rowDict["insert_time"] = rowDict["insert_time"].split(".")[0]
    if type(rowDict["publish_company_id"]) is not int:
        rowDict["publish_company_id"] = 0
    if type(rowDict["ad_company_id"]) is not int:
        rowDict["ad_company_id"] = 0
    if type(rowDict["clue_id"]) is not str:
        rowDict["clue_id"] = ""
    if type(rowDict["ad_num"]) is not int:
        rowDict["ad_num"] = 0
    if type(rowDict["special_name"]) is not str:
        rowDict["special_name"] = ""
    if type(rowDict["collect_time"]) is not str:
        rowDict["collect_time"] = base_time
    rowDict["collect_time"] = rowDict["collect_time"]
    if type(rowDict["ad_reg_institute"]) is not str:
        rowDict["ad_reg_institute"] = ""
    if type(rowDict["publish_reg_institute"]) is not str:
        rowDict["publish_reg_institute"] = ""
    # ads_review表的create_time
    rowDict["year"] = ""
    rowDict["month"] = ""
    rowDict["ds"] = ""
    rowDict["ads_review_create_time"] = base_time
    rowDict["ads_review_status"] = ""
    rowDict["ads_review_user"] = ""
    rowDict["ads_review_result"] = ""
    rowDict["ads_handle_status"] = ""
    rowDict["ads_handle_result"] = ""
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
    tableName = "sh2_urlsafe.t_ad_urlsafe_fakeads_engine_ads_check_distinct_total_shenzhen_v1"
    selectFields = "id,ad_global_id,ad_signature,ad_obj_type,ad_obj_key,ad_obj_name,ad_name,ad_text,ad_pic,ad_pics_cos," \
                   "ad_vedio,ad_vedios_cos,ad_appear_url,ad_appear_site,ad_appear_domain,ad_appear_url_title,ad_appear_url_snapshot," \
                   "ad_click_url,ad_click_site,ad_click_domain,ad_land_url,ad_land_site,ad_land_domain,ad_land_url_title,ad_land_url_body," \
                   "ad_land_url_snapshot,publish_company,publish_icp_type,publish_icp_num,publish_province,publish_city,publish_area," \
                   "publish_address,ad_agent,ad_company,ad_icp_type,ad_icp_num,ad_province,ad_city,ad_area,ad_address,detect_ad_type," \
                   "detect_sub_type,detect_result,detect_keywords,detect_reason,detect_law_code,detect_law_src,detect_law_label," \
                   "detect_law_detail,crawler_ip,crawler_country,crawler_province,crawler_city,insert_time,publish_company_id,ad_company_id," \
                   "clue_id,ad_num,special_name,collect_time,ad_reg_institute,publish_reg_institute,year,month,ds,ads_review_create_time," \
                   "ads_review_status,ads_review_user,ads_review_result,ads_handle_status,ads_handle_result"
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
