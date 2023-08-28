package turl

import (
	"net/url"
)

// NormURL 标准化URL，待优化
func NormURL(inputURL string) (u *url.URL, err error) {
	u, err = url.Parse(inputURL)
	return
}
