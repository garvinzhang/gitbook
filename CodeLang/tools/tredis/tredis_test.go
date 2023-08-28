package tredis

import (
	"context"
	"testing"
	"time"

	"git.code.oa.com/rainbow/golang-sdk/log"
)

func TestDel(t *testing.T) {
	var ctx = context.Background()
	rdb, err := InitRedis("", "", 0)
	if err != nil {
		t.Fatal(err)
	}
	n, err := rdb.Del(ctx, "key1").Result()
	if err != nil {
		t.Fatal(err)
	}
	log.Info(n)
}
func TestExists(t *testing.T) {
	var ctx = context.Background()
	rdb, err := InitRedis("", "", 0)
	if err != nil {
		t.Fatal(err)
	}
	n, err := rdb.Exists(ctx, "key1").Result()
	if err != nil {
		t.Fatal(err)
	}
	log.Info(n) //n>0 exists;
}

func TestExpire(t *testing.T) {
	var ctx = context.Background()
	rdb, err := InitRedis("", "", 0)
	if err != nil {
		t.Fatal(err)
	}
	ok, err := rdb.Expire(ctx, "key1", time.Minute*2).Result()
	if err != nil {
		t.Fatal(err)
	}
	if !ok {
		t.Log("set expire failed")
	}

	ok, err = rdb.ExpireAt(ctx, "key2", time.Now().AddDate(0, 0, 7)).Result()
	if err != nil {
		t.Fatal(err)
	}
	if !ok {
		t.Log("set expire failed")
	}
}

func TestSet(t *testing.T) {
	//Set方法的最后一个参数表示过期时间，0表示永不过期
	// err = rdb.Set(ctx, "key1", "value1", 0).Err()
	// if err != nil {
	// 	panic(err)
	// }
	// //key2将会在两分钟后过期失效
	// err = rdb.Set(ctx, "key2", "value2", time.Minute*2).Err()
	// if err != nil {
	// 	panic(err)
	// }
}

func TestGet(t *testing.T) {
	// if err == redis.Nil {
	// 	fmt.Println("key不存在")
	// } else if err != nil {
	// 	panic(err)
	// } else {
	// 	fmt.Printf("值为: %v\n", val2)
	// }
}
