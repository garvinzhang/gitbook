package trainbow

import (
	"testing"

	"git.code.oa.com/trpc-go/trpc-go/log"
)

type ConfTestTools struct {
	Email string `yaml:"email"`
	Qywx  string `yaml:"qywx"`
}

func TestRainbow(t *testing.T) {
	InitRainbow("c228a2d5-bfcb-4ba5-b13e-63b439a94675", "d8a0159e3e554f90b700fdfeff084b01", "15f855d2d510d357bdbf8bb2ba86a8dfaa9a", "GolangDev", "Default")
	var confTestTools ConfTestTools
	_ = GetRainbowConfig("TestTools", &confTestTools)
	log.Infof("%+v", confTestTools)
}
