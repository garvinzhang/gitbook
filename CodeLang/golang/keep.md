# 日常发现记录

## 2023年08月

### 11日17:15

- Golang ENV 环境

Golang在安装的默认proxy是`GOPROXY="https://proxy.golang.org,direct"`，通过`go env`命令查看，但是由于网络（直连）问题，在安装包的时候会超时报错，所以需要更改成国内代理，通过命令`go env -w GOPROXY=https://goproxy.cn,direct`进行修改

