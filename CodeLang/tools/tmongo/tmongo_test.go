package tmongo

import (
	"context"
	"strconv"
	"testing"
	"unicode/utf8"

	"git.code.oa.com/trpc-go/trpc-go/log"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func TestConnect(t *testing.T) {
	uri := ""
	mongoClient, err := InitMongo(uri)
	if err != nil {
		log.Fatal(err)
	}
	collection := mongoClient.Database("").Collection("")
	log.Info(collection)
}

func TestDisconnect(t *testing.T) {
	var client *mongo.Client
	_ = client.Disconnect(context.TODO())
}

func TestFindOne(t *testing.T) {
	var collection *mongo.Collection
	filter := bson.D{{"nick_name", "水滴筹"}}
	var data TOaDistinctTotal
	_ = collection.FindOne(context.TODO(), filter).Decode(&data)
	log.Infof("%+v", data)
}

// TestFind1 游标逐个读取，节省内存
func TestFind1(t *testing.T) {
	var collection *mongo.Collection
	filter := bson.D{{"date_ds", bson.D{{"$lt", 20230101}}}}
	findOptions := options.Find()
	findOptions.SetLimit(5)
	cur, err := collection.Find(context.TODO(), filter, findOptions)
	if err != nil {
		log.Fatal(err)
	}
	for cur.Next(context.TODO()) {
		var data TOaDistinctTotal
		err := cur.Decode(&data)
		if err != nil {
			log.Fatal(err)
		}
		log.Infof("%+v", data)
	}
	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}
	cur.Close(context.TODO())
}

// TestFind2 一次性加载到内存中
func TestFind2(t *testing.T) {
	var collection *mongo.Collection
	filter := bson.D{{"date_ds", bson.D{{"$lt", 20230101}}}}
	findOptions := options.Find()
	findOptions.SetLimit(5)
	cur, err := collection.Find(context.TODO(), filter, findOptions)
	if err != nil {
		log.Fatal(err)
	}
	var datas []TOaDistinctTotal
	if err = cur.All(context.TODO(), &datas); err != nil {
		panic(err)
	}
	for _, data := range datas {
		log.Infof("%+v", data)
	}
}

// TOaDistinctTotal  去重全量微信公众号主体库（更新）
type TOaDistinctTotal struct {
	ID                  int64  `bson:"id"`                    //  自增计数
	ArticleUrl          string `bson:"article_url"`           //  示例文章链接
	WxmpBiz             string `bson:"wxmp_biz"`              //  公众号biz
	NickName            string `bson:"nick_name"`             //  公众号昵称
	UserName            string `bson:"user_name"`             //  公众号作者微信号
	HeadImgOri          string `bson:"head_img_ori"`          //  公众号logo清晰大图
	HeadImgRound        string `bson:"head_img_round"`        //  公众号logo圆图
	HeadImgCos          string `bson:"head_img_cos"`          //  公众号logocos链接
	ArticleTitle        string `bson:"article_title"`         //  示例文章标题
	Account             string `bson:"account"`               //  公众号帐号
	Intro               string `bson:"intro"`                 //  公众号简介
	QrCode              string `bson:"qr_code"`               //  公众号关注二维码
	IcpType             string `bson:"icp_type"`              //  公众号icp类型
	IcpCompany          string `bson:"icp_company"`           //  公众号公司
	ServiceType         string `bson:"service_type"`          //  公众号服务类型
	IpProvince          string `bson:"ip_province"`           //  公众号ip省份
	PhoneNumber         string `bson:"phone_number"`          //  公众号联系电话
	BrandProtect        string `bson:"brand_protect"`         //  公众号品牌
	LicenseNum          string `bson:"license_num"`           //  公众号信用代码
	ApiService          string `bson:"api_service"`           //  公众号用到的三方接口公司
	RenameHistory       string `bson:"rename_history"`        //  公众号重命名历史
	VerifyName          string `bson:"verify_name"`           //  公司复核名称
	VerifyTime          string `bson:"verify_time"`           //  公司复核时间
	VerifyCompanyType   string `bson:"verify_company_type"`   //  公司复核公司类型
	VerifyFoundTime     string `bson:"verify_found_time"`     //  公司复核创建时间
	VerifyBusinessTime  string `bson:"verify_business_time"`  //  公司符合营业时间
	VerifyLicenseNum    string `bson:"verify_license_num"`    //  公司复核信用代码
	VerifyBusinessScope string `bson:"verify_business_scope"` //  公司复核营业范围
	CollectTimeStamp    int64  `bson:"collect_time_stamp"`    //  数据采集时间戳
	DateDs              int64  `bson:"date_ds"`               //  采集时间分区
	InsertTime          string `bson:"insert_time"`           //  插入时间
	UpdateTime          string `bson:"update_time"`           //  更新时间
}

func TestXxx(t *testing.T) {
	var num int64
	var datas []TOaDistinctTotal
	for num = 0; num < 5; num++ {
		var data TOaDistinctTotal
		data.CollectTimeStamp = num
		_ = data.clData()
		datas = append(datas, data)
	}
	for _, da := range datas {
		t.Logf("%+v", da)
	}
	t.Log(len(datas))
}

func (data *TOaDistinctTotal) clData() (err error) {
	if data.Account == "" {
		data.Account = "youzhicaixing"
	}
	log.Info(utf8.RuneCountInString("a啊师傅"))
	return
}

func TestSs(t *testing.T) {
	s := "a我😁cd"
	s = string([]rune(s)[:3])
	t.Log(s) //得到 "a我c"
}

func TestTAS(t *testing.T) {
	b := 1
	a := "啊师傅as " + strconv.Itoa(b)
	t.Log(a)
}
