package tmail

import (
	"fmt"
	"mime"

	"github.com/spf13/cast"
	"gopkg.in/gomail.v2"
)

// MailConf 邮箱配置参数
type MailConf struct {
	user     string
	pwd      string
	host     string
	port     string
	username string
}

// MessageConf 邮件内容配置参数
type MessageConf struct {
	mailTo     []string
	subject    string
	body       string
	attachPath string
	attachName string
}

var mailConf MailConf
var messageConf MessageConf

// InitMail 初始化邮箱
func InitMail(user, pwd, host, port, username string) {
	mailConf.user = user
	mailConf.pwd = pwd
	mailConf.host = host
	mailConf.port = port
	mailConf.username = username
}

// InitMessage 初始化邮件内容 mailTo: 收件人，subject: 主题 body: 正文内容 attach: 附件文件名（默认在当前路径下）
func InitMessage(mailTo []string, subject, body, attachPath, attachName string) {
	messageConf.mailTo = mailTo
	messageConf.subject = subject
	messageConf.body = body
	messageConf.attachPath = attachPath
	messageConf.attachName = attachName
}

// SendMail 先初始化两个Init，然后发送邮件
func SendMail() error {
	m := gomail.NewMessage()
	m.SetHeader("From", m.FormatAddress(mailConf.user, mailConf.username))
	m.SetHeader("To", messageConf.mailTo...)
	m.SetHeader("Subject", messageConf.subject)
	m.SetBody("text/html", messageConf.body)
	if messageConf.attachPath != "" {
		m.Attach(messageConf.attachPath, gomail.Rename(messageConf.attachName), gomail.SetHeader(map[string][]string{
			"Content-Disposition": {
				fmt.Sprintf(`attachment; filename="%s"`, mime.BEncoding.Encode("UTF-8", messageConf.attachName)),
			},
		}))
	}
	d := gomail.NewDialer(mailConf.host, cast.ToInt(mailConf.port), mailConf.user, mailConf.pwd)
	err := d.DialAndSend(m)
	return err
}
