package main

// TOaDistinctTotal  去重全量微信公众号主体库（更新）
type TOaDistinctTotal struct {
	ID                  int64  `db:"id" bson:"id"`                                       //  自增计数
	ArticleUrl          string `db:"article_url" bson:"article_url"`                     //  示例文章链接
	WxmpBiz             string `db:"wxmp_biz" bson:"wxmp_biz"`                           //  公众号biz
	NickName            string `db:"nick_name" bson:"nick_name"`                         //  公众号昵称
	UserName            string `db:"user_name" bson:"user_name"`                         //  公众号作者微信号
	HeadImgOri          string `db:"head_img_ori" bson:"head_img_ori"`                   //  公众号logo清晰大图
	HeadImgRound        string `db:"head_img_round" bson:"head_img_round"`               //  公众号logo圆图
	HeadImgCos          string `db:"head_img_cos" bson:"head_img_cos"`                   //  公众号logocos链接
	ArticleTitle        string `db:"article_title" bson:"article_title"`                 //  示例文章标题
	Account             string `db:"account" bson:"account"`                             //  公众号帐号
	Intro               string `db:"intro" bson:"intro"`                                 //  公众号简介
	QrCode              string `db:"qr_code" bson:"qr_code"`                             //  公众号关注二维码
	IcpType             string `db:"icp_type" bson:"icp_type"`                           //  公众号icp类型
	IcpCompany          string `db:"icp_company" bson:"icp_company"`                     //  公众号公司
	ServiceType         string `db:"service_type" bson:"service_type"`                   //  公众号服务类型
	IpProvince          string `db:"ip_province" bson:"ip_province"`                     //  公众号ip省份
	PhoneNumber         string `db:"phone_number" bson:"phone_number"`                   //  公众号联系电话
	BrandProtect        string `db:"brand_protect" bson:"brand_protect"`                 //  公众号品牌
	LicenseNum          string `db:"license_num" bson:"license_num"`                     //  公众号信用代码
	ApiService          string `db:"api_service" bson:"api_service"`                     //  公众号用到的三方接口公司
	RenameHistory       string `db:"rename_history" bson:"rename_history"`               //  公众号重命名历史
	VerifyName          string `db:"verify_name" bson:"verify_name"`                     //  公司复核名称
	VerifyTime          string `db:"verify_time" bson:"verify_time"`                     //  公司复核时间
	VerifyCompanyType   string `db:"verify_company_type" bson:"verify_company_type"`     //  公司复核公司类型
	VerifyFoundTime     string `db:"verify_found_time" bson:"verify_found_time"`         //  公司复核创建时间
	VerifyBusinessTime  string `db:"verify_business_time" bson:"verify_business_time"`   //  公司符合营业时间
	VerifyLicenseNum    string `db:"verify_license_num" bson:"verify_license_num"`       //  公司复核信用代码
	VerifyBusinessScope string `db:"verify_business_scope" bson:"verify_business_scope"` //  公司复核营业范围
	CollectTimeStamp    int64  `db:"collect_time_stamp" bson:"collect_time_stamp"`       //  数据采集时间戳
	DateDs              int64  `db:"date_ds" bson:"date_ds"`                             //  采集时间分区
	InsertTime          string `db:"insert_time" bson:"insert_time"`                     //  插入时间
	UpdateTime          string `db:"update_time" bson:"update_time"`                     //  更新时间
}
