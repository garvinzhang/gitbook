package tagent

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"

	"git.code.oa.com/trpc-go/trpc-go/log"
)

// Msg 消息体
type Msg struct {
	MsgType  string `json:"msgtype"`
	Markdown MD     `json:"markdown"`
}

// MD markdown结构体
type MD struct {
	MentionedList []string `json:"mentioned_list"`
	Content       string   `json:"content"`
}

// sendMsg 发送企业微信消息
func SendMsg(apiKey, content, mention string) (err error) {
	url := "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + apiKey
	if mention != "" {
		content = fmt.Sprintf("%s\n<@%s>", content, mention)
	}
	msg := Msg{
		MsgType: "markdown",
		Markdown: MD{
			MentionedList: []string{},
			Content:       content,
		},
	}
	msgByte, _ := json.Marshal(msg)
	resp, err := http.Post(url, "application/json", bytes.NewReader(msgByte))
	if err != nil {
		log.Error("qywxAgentErr:", err)
	}
	defer resp.Body.Close()
	return
}
