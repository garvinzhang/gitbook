package main

import (
	"context"
	"fmt"
	"strconv"
	"unicode/utf8"

	"git.code.oa.com/trpc-go/trpc-go/log"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"

	"git.woa.com/vhukzhang/tools/tmongo"
	"git.woa.com/vhukzhang/tools/tmysql"
	"git.woa.com/vhukzhang/tools/ttime"
)

const (
	dsn          = ""
	uri          = ""
	tableName    = "base.t_oa_distinct_total"
	selectFileds = ` id,offline_time,offline_apply_time,offline_note,is_false,insert_time,update_time `
	insertFileds = ` article_url,wxmp_biz,nick_name,user_name,head_img_ori,head_img_round,head_img_cos, 
                     article_title,account,intro,qr_code,icp_type,icp_company,service_type,ip_province, 
                     phone_number,brand_protect,license_num,api_service,rename_history,verify_name, 
                     verify_time,verify_company_type,verify_found_time,verify_business_time,verify_license_num, 
                     verify_business_scope,collect_time_stamp,date_ds,insert_time,update_time `
	insertValues = ` :article_url,:wxmp_biz,:nick_name,:user_name,:head_img_ori,:head_img_round, 
                     :head_img_cos,:article_title,:account,:intro,:qr_code,:icp_type,:icp_company, 
                     :service_type,:ip_province,:phone_number,:brand_protect,:license_num,:api_service, 
                     :rename_history,:verify_name,:verify_time,:verify_company_type,:verify_found_time, 
                     :verify_business_time,:verify_license_num,:verify_business_scope,:collect_time_stamp, 
                     :date_ds,:insert_time,:update_time `
)

func Tmain() {
	ds1 := ttime.GetDateDs(-1)
	ds2 := ttime.GetDateDs(0)
	var num int
	mdb, err := tmysql.InitMysql(dsn)
	if err != nil {
		log.Fatal(err)
	}
	mongoClient, err := tmongo.InitMongo(uri)
	if err != nil {
		log.Fatal(err)
	}
	collection := mongoClient.Database("regbase").Collection("offical_account_detail")
	filter := bson.D{
		{"$and",
			bson.A{
				bson.D{{"date_ds", bson.D{{"$gte", ds1}}}},
				// bson.D{{"date_ds", bson.D{{"$lt", 20230101}}}},
				// bson.D{{"date_ds", bson.D{{"$gte", 20230101}}}},
				bson.D{{"date_ds", bson.D{{"$lt", ds2}}}},
			},
		},
	}
	// filter := bson.D{{}}
	findOptions := options.Find()
	// findOptions.SetLimit(3578)
	// findOptions.SetSort(bson.D{{"date_ds", 1}})
	cur, err := collection.Find(context.TODO(), filter, findOptions)
	if err != nil {
		log.Fatal(err)
	}
	dupStr := tmysql.ExtraDupStr(insertFileds)
	sqlStr := fmt.Sprintf("INSERT INTO %s(%s)VALUES(%s) ON DUPLICATE KEY UPDATE %s", tableName, insertFileds, insertValues, dupStr)
	datas := []TOaDistinctTotal{}
	for cur.Next(context.TODO()) {
		num++
		var data TOaDistinctTotal
		err := cur.Decode(&data)
		if err != nil {
			log.Warn(err)
			continue
		}
		// 清洗结构体-长度过长 批量插入 uk跳过逻辑
		data.cleanData()
		datas = append(datas, data)
		if num%1000 == 0 {
			log.Infof("HandleNum:%d|%d", num, len(datas))
			_, err = mdb.NamedExec(sqlStr, datas)
			if err != nil {
				log.Warn(err)
			}
			// 清空datas
			datas = []TOaDistinctTotal{}
		}
	}
	log.Infof("LastHandleNum:%d|%d", num, len(datas))
	_, err = mdb.NamedExec(sqlStr, datas)
	if err != nil {
		log.Warn(err)
	}
	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}
	cur.Close(context.TODO())
}

func (data *TOaDistinctTotal) cleanData() {
	data.ArticleUrl = splitStr(data.ArticleUrl, 510)
	data.WxmpBiz = splitStr(data.WxmpBiz, 30)
	data.NickName = splitStr(data.NickName, 250)
	data.UserName = splitStr(data.UserName, 60)
	data.HeadImgOri = splitStr(data.HeadImgOri, 510)
	data.HeadImgRound = splitStr(data.HeadImgRound, 510)
	data.HeadImgCos = splitStr(data.HeadImgCos, 510)
	data.ArticleTitle = splitStr(data.ArticleTitle, 250)
	data.Account = splitStr(data.Account, 250)
	data.Intro = splitStr(data.Intro, 1020)
	data.QrCode = splitStr(data.QrCode, 120)
	data.IcpType = splitStr(data.IcpType, 120)
	data.IcpCompany = splitStr(data.IcpCompany, 510)
	data.ServiceType = splitStr(data.ServiceType, 250)
	data.IpProvince = splitStr(data.IpProvince, 120)
	data.PhoneNumber = splitStr(data.PhoneNumber, 60)
	data.BrandProtect = splitStr(data.BrandProtect, 510)
	data.LicenseNum = splitStr(data.LicenseNum, 250)
	data.ApiService = splitStr(data.ApiService, 510)
	data.RenameHistory = splitStr(data.RenameHistory, 1020)
	data.VerifyName = splitStr(data.VerifyName, 510)
	data.VerifyTime = splitStr(data.VerifyTime, 250)
	data.VerifyCompanyType = splitStr(data.VerifyCompanyType, 510)
	data.VerifyFoundTime = splitStr(data.VerifyFoundTime, 250)
	data.VerifyBusinessTime = splitStr(data.VerifyBusinessTime, 250)
	data.VerifyLicenseNum = splitStr(data.VerifyLicenseNum, 250)
	data.VerifyBusinessScope = splitStr(data.VerifyBusinessScope, 1020)
}

func splitStr(oriStr string, len int) string {
	if utf8.RuneCountInString(oriStr) > len {
		splStr := string([]rune(oriStr)[:len])
		return splStr
	}
	return oriStr
}

func DInsert() {
	mdb, err := tmysql.InitMysql(dsn)
	if err != nil {
		log.Fatal(err)
	}
	dupStr := tmysql.ExtraDupStr(insertFileds)
	sqlStr := fmt.Sprintf("INSERT INTO %s(%s)VALUES(%s) ON DUPLICATE KEY UPDATE %s", tableName, insertFileds, insertValues, dupStr)

	datas := []TOaDistinctTotal{}
	for i := 0; i < 3; i++ {
		var data TOaDistinctTotal
		data.WxmpBiz = "UKBiz1" + strconv.Itoa(i)
		data.NickName = "UKName1"
		data.UpdateTime = ttime.GetDateTime(0)
		data.InsertTime = ttime.GetDateTime(-1)
		datas = append(datas, data)
	}
	// rsp, err := mdb.NamedExec(sqlStr, data)
	rsp, err := mdb.NamedExec(sqlStr, datas)
	if err != nil {
		log.Fatal(err)
	}
	log.Infof("%v", rsp)

	datas = []TOaDistinctTotal{}
	for i := 0; i < 3; i++ {
		var data TOaDistinctTotal
		data.WxmpBiz = "UKBizsss"
		data.NickName = "UKName1"
		data.UpdateTime = ttime.GetDateTime(0)
		data.InsertTime = ttime.GetDateTime(-1)
		datas = append(datas, data)
	}
	rsp, err = mdb.NamedExec(sqlStr, datas)
	if err != nil {
		log.Fatal(err)
	}
	log.Infof("%v", rsp)
}

func main() {
	log.Info("main")
	// DInsert()
	// test limit
	Tmain()
}
