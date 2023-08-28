package ttime

import "testing"

func TestGetDateTime(t *testing.T) {
	dateTime := GetDateTime(0)
	t.Log(dateTime)
}

func TestGetDate(t *testing.T) {
	date := GetDate(0)
	t.Log(date)
}

func TestGetDateDs(t *testing.T) {
	dateDs := GetDateDs(-1)
	t.Log(dateDs)
}
