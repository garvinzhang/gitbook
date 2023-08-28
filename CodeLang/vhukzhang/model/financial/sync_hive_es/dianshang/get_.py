column_list = [
    "id bigint COMMENT '',",
    "goods_id string COMMENT '商品ID',",
    "goods_title string COMMENT '商品名称',",
    "goods_dst_url string COMMENT '商品最终目的URL',",
    "goods_origin_url string COMMENT '商品爬取源URL',",
    "goods_detail string COMMENT '商品描述细节',",
    "goods_detail_img_urls string COMMENT '商品详情 图片链接',",
    "goods_detail_img_ocr string COMMENT '商品详情图ocr文本',",
    "goods_main_img_ocr string COMMENT '商品主图ocr文本',",
    "goods_mainimg_urls string COMMENT '商品主图图片链接',",
    "price bigint COMMENT '价格（分）',",
    "original_price bigint COMMENT '原价（分）',",
    "sales_type tinyint COMMENT '销量类型，-1:未知\;0:总销量\;1:月销量',",
    "goods_sales_count bigint COMMENT '商品销量',",
    "goods_sales_amount bigint COMMENT '商品销售额',",
    "goods_stock bigint COMMENT '商品库存',",
    "deliver_province string COMMENT '发货省',",
    "deliver_city string COMMENT '发货市',",
    "deliver_area string COMMENT '发货区',",
    "brand_category string COMMENT '品牌类别',",
    "brand_id string COMMENT '品牌ID',",
    "brand_name string COMMENT '品牌名称',",
    "cate_level1_id bigint COMMENT '一级类目ID',",
    "cate_level1_name string COMMENT '一级类目名称',",
    "cate_level2_id bigint COMMENT '二级类目ID',",
    "cate_level2_name string COMMENT '二级类目名称',",
    "cate_level3_id bigint COMMENT '三级类目ID',",
    "cate_level3_name string COMMENT '三级类目名称',",
    "cate_level4_id bigint COMMENT '四级类目ID',",
    "cate_level4_name string COMMENT '四级类目名称',",
    "cate_level5_id bigint COMMENT '五级类目ID',",
    "cate_level5_name string COMMENT '五级类目名称',",
    "comments bigint COMMENT '评论数',",
    "good_comments bigint COMMENT '好评量',",
    "mid_comments bigint COMMENT '中评量',",
    "bad_comments bigint COMMENT '差评量',",
    "sku_info string COMMENT '商品型号信息',",
    "platform_id bigint COMMENT '平台ID, 对应monitor_platform_info中的id',",
    "platform_name string COMMENT '平台名称',",
    "shop_id string COMMENT '店铺ID',",
    "shop_name string COMMENT '店铺名称',",
    "task_src string COMMENT '项目指定的\n例如：\n贵阳| 天津 | 浦东',",
    "goods_other_info string COMMENT '商品的其他信息，以json格式进行存储',",
    "company_id bigint COMMENT '公司id',",
    "company_name string COMMENT '公司名字',",
    "province string COMMENT '企业省',",
    "city string COMMENT '企业市',",
    "area string COMMENT '企业区',",
    "obj_type string COMMENT '监测平台类型',",
    "insert_time string COMMENT '生成时间"
]


# 获取Elasticsearch索引语句框架
def get_index():
    for column in column_list:
        # 数据类型
        dataTypeStartString = column.split(" ")[1]
        index_string = "\"" + column.split(" ")[0] + "\"" + ":{\n"
        if dataTypeStartString.startswith('bigint'):
            index_string = index_string + " \"type\" : \"long\"\n"
        elif dataTypeStartString.startswith('string'):
            index_string = index_string + " \"type\" : \"keyword\"\n"
        elif dataTypeStartString.startswith('int'):
            index_string = index_string + " \"type\" : \"integer\"\n"
        index_string = index_string + "},"
        print(index_string)


def get_column_string():
    column_string = ''
    for column in column_list:
        column_string += column.split(" ")[0] + ','
    return column_string[:len(column_string) - 1]


def getCode():
    index_string = ''
    for column in column_list:
        dataTypeStartString = column.split(" ")[1]
        column_name = column.split(" ")[0]
        if dataTypeStartString.startswith('bigint'):
            index_string = f"""    if type(rowDict["{column_name}"]) is not int:
        rowDict["{column_name}"] = 0"""
        elif dataTypeStartString.startswith('string'):
            index_string = f"""    if type(rowDict["{column_name}"]) is not str:
                    rowDict["{column_name}"] = \"\""""
        elif dataTypeStartString.startswith('int'):
            index_string = f"""    if type(rowDict["{column_name}"]) is not int:
                    rowDict["{column_name}"] = 0"""
        print(index_string)



if __name__ == "__main__":
    print(get_column_string())
    get_index()
    getCode()
