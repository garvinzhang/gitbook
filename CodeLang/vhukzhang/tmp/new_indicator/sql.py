ds = 20230313
# start_ds = "%LASTDAY_15%"
# end_ds = "%LASTDAY%"
start_ds = "20230301"
end_ds = "20230313"
title_regex = "(?=.*((\\b|[^\\x00-\\xff])(VR|AR)(\\b|[^\\x00-\\xff]))|(元宇宙))(?=.*(未来|布局|宣传|上线|公测|平台|下载|玩|如何|开发|研发))"
content_regex = "(元宇宙)"
limit_stmt = " LIMIT 1000 "

sql = f"""
SELECT
    {ds} as ds, 
    platform_name as platform, company_name as company, 
    url, title, body as content,
    if (coalesce(origin_id, '') !=  '', concat('wx:', coalesce(origin_id, ''), ', nick:', coalesce(nickname, '')), '') as extra_info
FROM (
    -- 寻找每个 url 中最合适的企业和平台    
    select
        min(ds) as ds, 
        url, title, body, 
        biz, origin_id, wxaccount, nickname,
        company_name, platform_name,
        row_number() over (partition by url order by pos_distance asc) as row_idx
    FROM (
        -- 涉及元宇宙的url中,建立平台-企业的关系
        SELECT
            u.ds, u.url, u.title, u.body,
            u.biz, u.account_id as origin_id, u.account as wxaccount, u.nickname,
            company_entitie.name as company_name, company_entitie.startidx as company_name_pos,
            platform_entitie.name as platform_name, platform_entitie.startidx as platform_name_pos,
            abs(company_entitie.startidx - platform_entitie.startidx) as pos_distance    -- 企业名和平台名的距离
        FROM
            urlsafe.t_od_urlsafe_ep_url_content_mixed u
            LATERAL VIEW explode(content_entities) e1 as company_entitie
            LATERAL VIEW explode(content_entities) e2 as platform_entitie
        WHERE
            (u.ds BETWEEN {start_ds} AND {end_ds})
            and url not like '%mp.weixin.qq.com/s?src=%'   -- 暂时过滤掉微信公众号临时链接
            and company_entitie.type = "company"
            and platform_entitie.type = "platform"
            and abs(company_entitie.startidx - platform_entitie.startidx) <= 50
            and (title rlike '{title_regex}')
            and (body rlike '{content_regex}')  -- 元宇宙关键词
        {limit_stmt}
    ) u
    group by url, title, body, company_name, platform_name, biz, origin_id, wxaccount, nickname, pos_distance
) t 
WHERE row_idx = 1
{limit_stmt}
"""

print(sql)
