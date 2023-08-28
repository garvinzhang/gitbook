package tcos

import (
	"context"
	"fmt"
	"net/http"
	"net/url"

	"github.com/tencentyun/cos-go-sdk-v5"
)

// https://km.woa.com/articles/show/540789?kmref=search&from_page=1&no=3#go-sdk

// COSConf 对象存储的配置变量
type COSConf struct {
	Bucket    string
	Appid     string
	COSRegion string
	SecretId  string
	SecretKey string
}

func InitCOS(cosConf COSConf) (client *cos.Client) {
	bucketStr := fmt.Sprintf("http://%s-%s.cos-internal.%s.tencentcos.cn", cosConf.Bucket, cosConf.Appid, cosConf.COSRegion)
	u, _ := url.Parse(bucketStr)
	su, _ := url.Parse("http://service.cos.tencentcos.cn")
	b := &cos.BaseURL{BucketURL: u, ServiceURL: su}
	client = cos.NewClient(b, &http.Client{
		Transport: &cos.AuthorizationTransport{
			SecretID:  cosConf.SecretId,
			SecretKey: cosConf.SecretKey,
		},
	})
	return
}

func COSUpload(client *cos.Client, cosPath, localPath string, cosConf COSConf) (cosURL string, err error) {
	cosURL = fmt.Sprintf("https://%s-%s.cos.%s.myqcloud.com/%s", cosConf.Bucket, cosConf.Appid, cosConf.COSRegion, cosPath)
	_, _, err = client.Object.Upload(
		context.Background(), cosPath, localPath, nil,
	)
	return
}

func COSDownload(client *cos.Client, cosPath, localPath string) (err error) {
	opt := &cos.MultiDownloadOptions{
		ThreadPoolSize: 5,
	}
	_, err = client.Object.Download(
		context.Background(), cosPath, localPath, opt,
	)
	return
}
