package tagent

import (
	"testing"

	"git.woa.com/vhukzhang/tools/trainbow"
)

func TestSendMsg(t *testing.T) {
	apiKey := "xxxx-xxxx-..."
	content := "hello"
	mention := "" // 企业微信英文名 暂不支持@所有人 只可以@一个人
	err := SendMsg(apiKey, content, mention)
	t.Log(err)
}

type ConfTestTools struct {
	Email string `yaml:"email"`
	Qywx  string `yaml:"qywx"`
}

func TestSendMsgMy(t *testing.T) {
	trainbow.InitRainbow("c228a2d5-bfcb-4ba5-b13e-63b439a94675", "d8a0159e3e554f90b700fdfeff084b01", "15f855d2d510d357bdbf8bb2ba86a8dfaa9a", "GolangDev", "Default")
	var confTestTools ConfTestTools
	_ = trainbow.GetRainbowConfig("TestTools", &confTestTools)
	apiKey := confTestTools.Qywx
	t.Log(apiKey)
	content := "# title\n" +
		"**bold**\n" +
		"[这是一个链接](http://work.weixin.qq.com/api/doc)\n" +
		"`code` single line\n" +
		"> 文字\n" +
		"\n" +
		"<font color='info'>绿色</font>\n" +
		"<font color='comment'>灰色</font>\n" +
		"<font color='warning'>橙红色</font>"
	mention := "vhukzhang"
	err := SendMsg(apiKey, content, mention)
	t.Log(err)
}
