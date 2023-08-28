package ttime

import (
	"time"

	"github.com/spf13/cast"
)

const (
	DateTimeLayOut = "2006-01-02 15:04:05"
	DateLayOut     = "2006-01-02"
	DateDsLayOut   = "20060102"
)

// GetDate 获取从now开始后的day天日期
func GetDate(day int) string {
	return time.Now().AddDate(0, 0, day).Format(DateLayOut)
}

// GetDateTime 获取从now开始后的day天时间
func GetDateTime(day int) string {
	return time.Now().AddDate(0, 0, day).Format(DateTimeLayOut)
}

// GetDayInt 获取当前日期
func GetDateDs(day int) int {
	return cast.ToInt(time.Now().AddDate(0, 0, day).Format(DateDsLayOut))
}
