package tredis

import (
	"context"
	"time"

	"git.code.oa.com/trpc-go/trpc-go/log"
	"github.com/go-redis/redis/v8"
)

var ctx = context.Background()

//https://www.cnblogs.com/itbsl/p/14198111.html#%E8%BF%9E%E6%8E%A5redis

// InitRedis 初始化Init获取Redis，然后在业务代码中写一个GetRedis，使用这个rdb操作数据库即可
func InitRedis(addr, pwd string, db int) (rdb *redis.Client, err error) {
	rdb = redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: pwd,
		DB:       db,
	})
	_, err = rdb.Ping(ctx).Result()
	return
}

func Exists(rdb *redis.Client, key string) (ok bool) {
	n, err := rdb.Exists(ctx, key).Result()
	if err != nil {
		log.Error(err)
		return
	}
	if n > 0 {
		ok = true
	}
	return
}

func Del(rdb *redis.Client, key string) (err error) {
	_, err = rdb.Del(ctx, key).Result()
	return
}

func Set(rdb *redis.Client, key string, value interface{}, expiration time.Duration) (err error) {
	err = rdb.Set(ctx, key, value, expiration).Err()
	return
}

func SetNX(rdb *redis.Client, key string, value interface{}, expiration time.Duration) (ok bool) {
	res, err := rdb.SetNX(ctx, key, value, expiration).Result()
	if err != nil {
		log.Error(err)
		return
	}
	if res {
		ok = true
	}
	return
}

func Get(rdb *redis.Client, key string) (value string, err error) {
	value, err = rdb.Get(ctx, key).Result()
	return
}

func IncrBy(rdb *redis.Client, key string, num int64) (value int64, err error) {
	value, err = rdb.IncrBy(ctx, key, num).Result()
	return
}

func LPush(rdb *redis.Client, key string, values ...interface{}) (len int64, err error) {
	len, err = rdb.LPush(ctx, "list", 1, 2, 3).Result()
	return
}

func LLen(rdb *redis.Client, key string) (len int64, err error) {
	len, err = rdb.LLen(ctx, key).Result()
	return
}

func LPop(rdb *redis.Client, key string) (value string, err error) {
	value, err = rdb.LPop(ctx, key).Result()
	return
}

func BLPop(rdb *redis.Client, expiration time.Duration, key string) (value []string, err error) {
	value, err = rdb.BLPop(ctx, expiration, key).Result()
	return
}
