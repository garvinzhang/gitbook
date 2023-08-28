package tmysql

import (
	"fmt"
	"regexp"
	"strings"
	"testing"

	"git.code.oa.com/trpc-go/trpc-go/log"
)

const InsertFileds = ` article_url,wxmp_biz,nick_name,user_name,head_img_ori,head_img_round,head_img_cos, 
					   verify_business_scope,collect_time_stamp,date_ds,insert_time,update_time `

func TestMysql(t *testing.T) {
	dsn := "xxxx"
	mdb, err := InitMysql(dsn)
	if err != nil {
		log.Fatal(err)
	}
	var name string
	sqlStr := "SELECT name FROM student WHERE id=1"
	mdb.Get(&name, sqlStr)
}

func TestExtraDupStr(t *testing.T) {
	reg := regexp.MustCompile("\\s+")
	baseStr := reg.ReplaceAllString(InsertFileds, "")
	filedsList := strings.Split(baseStr, ",")
	var dupStr string
	for _, v := range filedsList {
		t.Log(v)
		dupStr += fmt.Sprintf("%s=VALUES(%s),", v, v)
	}
	dupStr = strings.TrimSuffix(dupStr, ",")
	t.Log(dupStr)
}
