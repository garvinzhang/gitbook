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
    "index": "goods_info_total",
}
REPARTITION_NUM = 200
# LIMIT = "LIMIT 1000000"
LIMIT = ""


def cleanType(rowDict: Dict) -> Dict:
    base_time = "1970-01-01 00:00:00"
    if type(rowDict["id"]) is not int:
        rowDict["id"] = 0
    if type(rowDict["goods_id"]) is not str:
        rowDict["goods_id"] = ""
    if type(rowDict["goods_title"]) is not str:
        rowDict["goods_title"] = ""
    if type(rowDict["goods_dst_url"]) is not str:
        rowDict["goods_dst_url"] = ""
    if type(rowDict["goods_origin_url"]) is not str:
        rowDict["goods_origin_url"] = ""
    if type(rowDict["goods_detail"]) is not str:
        rowDict["goods_detail"] = ""
    if type(rowDict["goods_detail_img_urls"]) is not str:
        rowDict["goods_detail_img_urls"] = ""
    if type(rowDict["goods_detail_img_ocr"]) is not str:
        rowDict["goods_detail_img_ocr"] = ""
    if type(rowDict["goods_main_img_ocr"]) is not str:
        rowDict["goods_main_img_ocr"] = ""
    if type(rowDict["goods_main_img_urls"]) is not str:
        rowDict["goods_main_img_urls"] = ""
    if type(rowDict["price"]) is not int:
        rowDict["price"] = 0
    if type(rowDict["original_price"]) is not int:
        rowDict["original_price"] = 0
    if type(rowDict["original_price"]) is not int:
        rowDict["original_price"] = 0
    if type(rowDict["goods_sales_count"]) is not int:
        rowDict["goods_sales_count"] = 0
    if type(rowDict["goods_sales_amount"]) is not int:
        rowDict["goods_sales_amount"] = 0
    if type(rowDict["goods_stock"]) is not int:
        rowDict["goods_stock"] = 0
    if type(rowDict["deliver_province"]) is not str:
        rowDict["deliver_province"] = ""
    if type(rowDict["deliver_city"]) is not str:
        rowDict["deliver_city"] = ""
    if type(rowDict["deliver_area"]) is not str:
        rowDict["deliver_area"] = ""
    if type(rowDict["brand_category"]) is not str:
        rowDict["brand_category"] = ""
    if type(rowDict["brand_id"]) is not str:
        rowDict["brand_id"] = ""
    if type(rowDict["brand_name"]) is not str:
        rowDict["brand_name"] = ""
    if type(rowDict["cate_level1_id"]) is not int:
        rowDict["cate_level1_id"] = 0
    if type(rowDict["cate_level1_name"]) is not str:
        rowDict["cate_level1_name"] = ""
    if type(rowDict["cate_level2_id"]) is not int:
        rowDict["cate_level2_id"] = 0
    if type(rowDict["cate_level2_name"]) is not str:
        rowDict["cate_level2_name"] = ""
    if type(rowDict["cate_level3_id"]) is not int:
        rowDict["cate_level3_id"] = 0
    if type(rowDict["cate_level3_name"]) is not str:
        rowDict["cate_level3_name"] = ""
    if type(rowDict["cate_level4_id"]) is not int:
        rowDict["cate_level4_id"] = 0
    if type(rowDict["cate_level4_name"]) is not str:
        rowDict["cate_level4_name"] = ""
    if type(rowDict["cate_level5_id"]) is not int:
        rowDict["cate_level5_id"] = 0
    if type(rowDict["cate_level5_name"]) is not str:
        rowDict["cate_level5_name"] = ""
    if type(rowDict["comments"]) is not int:
        rowDict["comments"] = 0
    if type(rowDict["good_comments"]) is not int:
        rowDict["good_comments"] = 0
    if type(rowDict["mid_comments"]) is not int:
        rowDict["mid_comments"] = 0
    if type(rowDict["bad_comments"]) is not int:
        rowDict["bad_comments"] = 0
    if type(rowDict["sku_info"]) is not str:
        rowDict["sku_info"] = ""
    if type(rowDict["platform_id"]) is not int:
        rowDict["platform_id"] = 0
    if type(rowDict["platform_name"]) is not str:
        rowDict["platform_name"] = ""
    if type(rowDict["shop_id"]) is not str:
        rowDict["shop_id"] = ""
    if type(rowDict["shop_name"]) is not str:
        rowDict["shop_name"] = ""
    if type(rowDict["task_src"]) is not str:
        rowDict["task_src"] = ""
    if type(rowDict["goods_other_info"]) is not str:
        rowDict["goods_other_info"] = ""
    if type(rowDict["company_id"]) is not int:
        rowDict["company_id"] = 0
    if type(rowDict["company_name"]) is not str:
        rowDict["company_name"] = ""
    if type(rowDict["province"]) is not str:
        rowDict["province"] = ""
    if type(rowDict["city"]) is not str:
        rowDict["city"] = ""
    if type(rowDict["area"]) is not str:
        rowDict["area"] = ""
    if type(rowDict["obj_type"]) is not str:
        rowDict["obj_type"] = ""
    if type(rowDict["insert_time"]) is not str:
        rowDict["insert_time"] = base_time
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
    tableName = "sh2_urlsafe.t_ed_urlsafe_net_trade_ziyan_goods_info_total"
    selectFields = "id,goods_id,goods_title,goods_dst_url,goods_origin_url,goods_detail,goods_detail_img_urls,goods_detail_img_ocr,goods_main_img_ocr,goods_mainimg_urls,price,original_price,sales_type,goods_sales_count,goods_sales_amount,goods_stock,deliver_province,deliver_city,deliver_area,brand_category,brand_id,brand_name,cate_level1_id,cate_level1_name,cate_level2_id,cate_level2_name,cate_level3_id,cate_level3_name,cate_level4_id,cate_level4_name,cate_level5_id,cate_level5_name,comments,good_comments,mid_comments,bad_comments,sku_info,platform_id,platform_name,shop_id,shop_name,task_src,goods_other_info,company_id,company_name,province,city,area,obj_type,insert_time"
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
