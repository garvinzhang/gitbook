package tmysql

import (
	"fmt"
	"regexp"
	"strings"

	"git.code.oa.com/trpc-go/trpc-go/log"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
)

// InitMysql 主函数Init获取mdb，然后在业务代码中写一个GetMdb的函数，使用这一个mdb操作数据库即可
func InitMysql(dsn string) (mdb *sqlx.DB, err error) {
	mdb = sqlx.MustConnect("mysql", dsn)
	err = mdb.Ping()
	return
}

// 增删改查 批量 使用示例

// Query 查询多个 游标读取 节省内存
func Query(mdb *sqlx.DB) {
	sqlStr := "SELECT a,b FROM table"
	rows, err := mdb.Query(sqlStr)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()
	for rows.Next() {
		var a, b string
		err = rows.Scan(&a, &b)
		if err != nil {
			log.Fatal(err)
		}
		log.Infof("a:%s|b:%s", a, b)
	}
}

// Exec 更改数据 插入数据 删除数据
func Exec(mdb *sqlx.DB) {
	sqlStr := "UPDATE table SET a=? WHERE id=?"
	sqlArgs := []interface{}{"a", "id"}
	_, err := mdb.Exec(sqlStr, sqlArgs...)
	if err != nil {
		log.Fatal(err)
	}
}

// Select 查询多行数据 一次性读取
func Select(mdb *sqlx.DB) {
	var dests []struct{}
	sqlStr := "SELECT * FROM table WHERE insert_time>='2021-01-01'"
	err := mdb.Select(&dests, sqlStr)
	if err != nil {
		log.Fatal(err)
	}
	for _, dest := range dests {
		log.Infof("%+v", dest)
	}
}

// Get 查询单个数据 结构体形式
func Get(mdb *sqlx.DB) {
	var dest struct{}
	sqlStr := "SELECT * FROM table WHERE id=?"
	sqlArgs := []interface{}{12}
	err := mdb.Get(dest, sqlStr, sqlArgs...)
	if err != nil {
		log.Fatal(err)
	}
	log.Infof("%+v", dest)
}

// ExtraDupStr
func ExtraDupStr(fileds string) (dupStr string) {
	reg := regexp.MustCompile("\\s+")
	baseStr := reg.ReplaceAllString(fileds, "")
	filedsList := strings.Split(baseStr, ",")
	for _, v := range filedsList {
		dupStr += fmt.Sprintf("%s=VALUES(%s),", v, v)
	}
	dupStr = strings.TrimSuffix(dupStr, ",")
	return
}
