# 获取hive urlsafe.t_td_urlsafe_new_qiye_company表的列string
# https://venus.woa.com/#/datas/metadata/show/434114
column_list = [
    "id bigint COMMENT '自增id', ",
    "cid bigint COMMENT '公司标识', ",
    "base string COMMENT '归属省份的首字母小写', ",
    "name string COMMENT '公司名称', ",
    "name_en string COMMENT '英文名', ",
    "name_alias string COMMENT '公司别名', ",
    "history_names string COMMENT '公司历史名称', ",
    "legal_entity_id bigint COMMENT '法人ID：人标识或公司标识', ",
    "legal_entity_type int COMMENT '法人类型，1 人 2 公司', ",
    "reg_number string COMMENT '注册号', ",
    "company_org_type string COMMENT '公司类型', ",
    "reg_location string COMMENT '注册地址', ",
    "estiblish_time string COMMENT '成立日期', ",
    "from_time string COMMENT '营业期限开始日期', ",
    "to_time string COMMENT '营业期限终止日期', ",
    "business_scope string COMMENT '经营范围', ",
    "reg_institute string COMMENT '登记机关', ",
    "approved_time string COMMENT '核准日期', ",
    "reg_status string COMMENT '企业状态', ",
    "reg_capital string COMMENT '注册资本', ",
    "org_number string COMMENT '组织机构代码', ",
    "org_approved_institute string COMMENT '组织机构批准单位', ",
    "current_cid bigint COMMENT '如果该条记录为历史名称，则该字段值对应最新名称那条记录的id', ",
    "parent_cid bigint COMMENT '上级机构ID', ",
    "company_type int COMMENT '机构类型-1:公司', ",
    "credit_code string COMMENT '统一社会信用代码', ",
    "score string COMMENT '公司评分', ",
    "category_code string COMMENT '行业分类', ",
    "lat string COMMENT '公司纬度', ",
    "lng string COMMENT '公司经度', ",
    "area_code int COMMENT '行政区划码', ",
    "reg_capital_amount bigint COMMENT '注册资本金额，数值类型', ",
    "reg_capital_currency string COMMENT '注册资本币种  人民币 美元 欧元 等', ",
    "actual_capital_amount bigint COMMENT '实收资本金额（单位：分）', ",
    "actual_capital_currency string COMMENT '实收资本币种 人民币 美元 欧元等', ",
    "reg_status_std string COMMENT '公司注册状态标准化', ",
    "social_security_staff_num int COMMENT '职工参保人数', ",
    "cancel_date string COMMENT '注销日期', ",
    "cancel_reason string COMMENT '注销原因', ",
    "revoke_date string COMMENT '吊销日期', ",
    "revoke_reason string COMMENT '吊销原因/吊销凭证', ",
    "emails string COMMENT '邮箱列表', ",
    "phones string COMMENT '电话', ",
    "wechat_public_num string COMMENT '微信公众号', ",
    "logo string COMMENT '公司logo', ",
    "crawled_time string COMMENT '解析完成时间', ",
    "create_time string COMMENT '创建时间', ",
    "update_time string COMMENT '更新时间', ",
    "deleted int COMMENT '是否删除，1:删除，0:未删除')"
]


def get_column_string():
    column_string = ''
    for column in column_list:
        column_string += column.split(" ")[0] + ','
    return column_string[:len(column_string) - 1]


if __name__ == "__main__":
    column_string = get_column_string()
    print(column_string)
