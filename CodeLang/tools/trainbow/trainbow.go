package trainbow

import (
	"git.code.oa.com/trpc-go/trpc-go/log"
	"gopkg.in/yaml.v3"

	"git.code.oa.com/rainbow/golang-sdk/confapi"
	"git.code.oa.com/rainbow/golang-sdk/keep"
	"git.code.oa.com/rainbow/golang-sdk/types"
)

var gval keep.Group

// InitRainbow 初始化七彩石Group的所有配置
func InitRainbow(appId, userId, userKey, group, env string) (err error) {
	rainbow, err := confapi.New(
		types.ConnectStr("http://api.rainbow.oa.com:8080"),
		types.IsUsingLocalCache(true),
		types.IsUsingFileCache(true),
		// 增加签名
		types.OpenSign(true), // 注意一定要开启后才会使用api签名
		types.AppID(appId),
		types.UserID(userId),
		types.UserKey(userKey),
		types.HmacWay("sha1"),
	)
	if err != nil {
		log.Warnf("[confapi.New]%s", err.Error())
		return
	}
	getOpts := make([]types.AssignGetOption, 0)
	getOpts = append(getOpts, types.WithGroup(group))
	getOpts = append(getOpts, types.WithEnvName(env))

	defer rainbow.Quit()
	gval, err = rainbow.GetGroup(getOpts...)
	if err != nil {
		log.Warnf("[rainbow.Get]%s", err.Error())
		return
	}
	return
}

// GetRainbowConfig 主函数内先Init完之后，一直调用此函数获取七彩石配置即可
func GetRainbowConfig(key string, value interface{}) (err error) {
	err = yaml.Unmarshal([]byte(gval[key].(string)), value)
	return
}
