package tmail

import (
	"os"
	"testing"

	"git.woa.com/vhukzhang/tools/trainbow"
)

func TestSendMail(t *testing.T) {
	InitMail("发件人邮箱", "发件人邮箱密码", "smtp.qq.com", "465", "发件人昵称")
	InitMessage([]string{"收件人邮箱"}, "标题", "正文", "test.jpg", "")
	err := SendMail()
	if err != nil {
		t.Fatal(err)
	}
}

type ConfTestTools struct {
	Email string `yaml:"email"`
	Qywx  string `yaml:"qywx"`
}

func TestSendMailMy(t *testing.T) {
	trainbow.InitRainbow("c228a2d5-bfcb-4ba5-b13e-63b439a94675", "d8a0159e3e554f90b700fdfeff084b01", "15f855d2d510d357bdbf8bb2ba86a8dfaa9a", "GolangDev", "Default")
	var confTestTools ConfTestTools
	_ = trainbow.GetRainbowConfig("TestTools", &confTestTools)
	dir, _ := os.Getwd()
	filePath := dir + "/test.png"
	emailPwd := confTestTools.Email
	fileName := "test.png"
	InitMail("garvinzhang@foxmail.com", emailPwd, "smtp.qq.com", "465", "发件人昵称")
	InitMessage([]string{"garvinszhang@outlook.com", "vhukzhang@tencent.com"}, "title", "body", filePath, fileName)
	err := SendMail()
	if err != nil {
		t.Fatal(err)
	}
}
