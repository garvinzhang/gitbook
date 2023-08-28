column_list = [
    "id bigint COMMENT 'id', ",
    "ad_global_id bigint COMMENT '从全量广告宽表里同步过来的id。\n用来回溯初始的广告数据状态\n例如【退回】操作，同步到初始的违规信息', ",
    "ad_signature string COMMENT '广告指纹，用于初步的去重，也可以看做是广告线索的唯一id\n使用url+title+body基于hash加密生成的32位码\n这个列的数据类型可能需要更改\n', ",
    "ad_obj_type string COMMENT '广告监测目标的类型\n例如：\n移动网页 | APP | 微信公众号 | 小程序 | 搜索引擎', ",
    "ad_obj_key string COMMENT '广告监测目标的id\n例如：\napp:填写包名，如com.rd.qnz | 公众号：填写公众号id,如gh_7c597a256261 | 网站：填写网站站点或者域名的URL', ",
    "ad_obj_name string COMMENT '广告监测目标的名称\n例如：墨迹天气 | 腾讯新闻网  等等', ",
    "ad_name string COMMENT '广告产品的名称\n例如：\n圣约翰草浸泡油', ",
    "ad_text string COMMENT '广告内容描述，广告文案摘要\n例如：\n山药双岐因子粉，健脾胃改善肠道微生态......本产品中含有的淮山药成分具有补肾益气的作用，山药双歧因子粉，提升自身免疫力......改善肠道微生态，促进钙吸收。提高机体免疫力，领钙入骨，促进骨代谢。', ",
    "ad_pic string COMMENT '广告宣传图的链接\n例如：\nhttps://item.taobao.com/item.htm?id=556838235725&ali_refid=a3_420435_1006:1151095640:N:aGK15LRvHNM0da22x5wT3Q%3D%3D:77f7347606e37eafd6c4197c11a1e88f&ali_trackid=1_77f7347606e37eafd6c4197c11a1e88f', ",
    "ad_pics_cos string COMMENT '广告宣传图的链接本地路径,多个链接用|分割', ",
    "ad_vedio string COMMENT '广告宣传音频的链接\n后续可能需要对视频、音频进行安全监管。\n如果有vedio信息，暂时先将这些信息进行保留\n', ",
    "ad_vedios_cos string COMMENT '广告宣传音频的链接，多个链接用|分割，\n后续可能需要对视频、音频进行安全监管。\n如果有vedio信息，暂时先将这些信息进行保留\n', ",
    "ad_appear_url string COMMENT '广告所在的页面链接\n有可能是新闻门户网站；也可能广告所在页与广告落地页相同', ",
    "ad_appear_site string COMMENT '广告所在页网页链接的站点名\n', ",
    "ad_appear_domain string COMMENT '广告所在页网页链接的域名\n', ",
    "ad_appear_url_title string COMMENT '广告所在页的网站标题', ",
    "ad_appear_url_snapshot string COMMENT '广告所在页的长截图链接', ",
    "ad_click_url string COMMENT '广告点击的页面链接\n点击的链接，有可能和落地页一样\n', ",
    "ad_click_site string COMMENT '广告点击页网页链接的站点名', ",
    "ad_click_domain string COMMENT '广告点击页网页链接的域名', ",
    "ad_land_url string COMMENT '广告落地页的链接', ",
    "ad_land_site string COMMENT '广告落地页网页链接的站点名', ",
    "ad_land_domain string COMMENT '广告落地页网页链接的域名', ",
    "ad_land_url_title string COMMENT '广告落地页的标题', ",
    "ad_land_url_body string COMMENT '广告落地页的文本内容', ",
    "ad_land_url_snapshot string COMMENT '广告落地页的长截图', ",
    "publish_company string COMMENT '互联网媒介，即广告发布者的公司名称', ",
    "publish_icp_type string COMMENT '互联网媒介，即广告发布者的icp\n例如：\n浙B2-20080224-1 等等', ",
    "publish_icp_num string COMMENT '互联网媒介，即广告发布者的icp例如：浙B2-20080224-1 等等', ",
    "publish_province string COMMENT '互联网媒介，即广告发布者的省', ",
    "publish_city string COMMENT '互联网媒介，即广告发布者的市', ",
    "publish_area string COMMENT '互联网媒介，即广告发布者的区', ",
    "publish_address string COMMENT '互联网媒介，即广告发布者的具体地理位置\n精确到XXXX路', ",
    "ad_agent string COMMENT '广告联盟，例如：\n广点通广告联盟 等等', ",
    "ad_company string COMMENT '广告主的公司名称', ",
    "ad_icp_type string COMMENT '广告主的icp\n例如：\n浙B2-20080224-1 等等', ",
    "ad_icp_num string COMMENT '广告主的icp备案类型，即广告主的icp类型例如：企业，个人等等', ",
    "ad_province string COMMENT '广告主的省', ",
    "ad_city string COMMENT '广告主的市', ",
    "ad_area string COMMENT '广告主的区', ",
    "ad_address string COMMENT '广告主的具体地理位置\n精确到街道', ",
    "detect_ad_type string COMMENT '违规广告类别：\n医疗服务类 | 药品类 | 房地产类 | 普通食品类 等等', ",
    "detect_sub_type string COMMENT '违规广告子类别：\n处方药 | 方便食品 | 调味品 等等', ",
    "detect_result bigint COMMENT '违规检测结果:0不违规，1违规', ",
    "detect_keywords string COMMENT '违规的关键词，关键词模型会有，机器学习模型中等同于detect_reason', ",
    "detect_reason string COMMENT '违规的那段文本内容\n一般是包含违规字段的一段文本', ",
    "detect_law_code string COMMENT '违规代码：\nYP1 | YP2 等等', ",
    "detect_law_src string COMMENT '违规来源：\n《广告法》第九条第二项；《药品管理法》第九十条第二款；《药品、医疗器械、保健食品、特殊医学用途配方食品广告审查管理暂行办法》第十一条第一项 \n| \n《广告法》第十六条第一款第二项\n等等', ",
    "detect_law_label string COMMENT '法律标签，竖线 | 分割多个', ",
    "detect_law_detail string COMMENT '违规细节：\n\n化妆品广告不得明示或者暗示产品具有医疗作用，不得含有虚假或者引人误解的内容，不得欺骗、误导消费者', ",
    "crawler_ip string COMMENT '采集机器的ip', ",
    "crawler_country string COMMENT '采集机器的国家：\n中国 | ', ",
    "crawler_province string COMMENT '采集机器的省份', ",
    "crawler_city string COMMENT '采集机器的城市', ",
    "insert_time string COMMENT '广告数据的入库时间', ",
    "publish_company_id bigint COMMENT '与company信息连接的外键', ",
    "ad_company_id bigint COMMENT '与company信息连接的外键', ",
    "clue_id string COMMENT '线索编号/条数编号', ",
    "ad_num int COMMENT '广告条次', ",
    "special_name string COMMENT '专项名称', ",
    "collect_time string COMMENT '采集时间', ",
    "ad_reg_institute string COMMENT '广告主登记机关', ",
    "publish_reg_institute string COMMENT '发布者登记机关')"
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
