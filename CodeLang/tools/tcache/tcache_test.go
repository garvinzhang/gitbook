package tcache

import (
	"runtime"
	"testing"

	"git.code.oa.com/trpc-go/trpc-go/log"
)

func TestS(t *testing.T) {
	pc, _, _, _ := runtime.Caller(1)
	name := runtime.FuncForPC(pc).Name()
	log.Info(name)
}
