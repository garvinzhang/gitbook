package tcos

import (
	"os"
	"testing"

	"git.code.oa.com/trpc-go/trpc-go/log"
)

func TestUpload(t *testing.T) {
	var cosConf COSConf
	cosConf.Appid = ""
	cosConf.Bucket = ""
	cosConf.COSRegion = ""
	cosConf.SecretId = ""
	cosConf.SecretKey = ""
	client := InitCOS(cosConf)

	cosPath := "url_crawl/wxmp_emu/aaa.png"
	dir, _ := os.Getwd()
	localPath := dir + "/aaa.png"
	cosURL, err := COSUpload(client, cosPath, localPath, cosConf)
	if err != nil {
		log.Fatal(err)
	}
	log.Info(cosURL)
}
