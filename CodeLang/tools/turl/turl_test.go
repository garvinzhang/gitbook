package turl

import "testing"

func TestNormURL(t *testing.T) {
	urlStr := "https://test:abcd123@golangbyexample.com:8000/tutorials/intro?type=advance&compact=false#history"
	u, err := NormURL(urlStr)
	if err != nil {
		t.Log(err)
	}
	t.Log(u.Scheme)
	t.Log(u.User)
	t.Log(u.Hostname())
	t.Log(u.Port())
	t.Log(u.Path)
	t.Log(u.RawQuery)
	t.Log(u.Fragment)
	t.Log(u.String())
}
