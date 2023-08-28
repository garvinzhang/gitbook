# 拉取基础镜像
FROM csighub.tencentyun.com/trpc-go/trpc-go-dev:latest
# FROM csighub.tencentyun.com/trpc-python/trpc-python-dev:latest

# 作者信息
LABEL MAINTAINER="vhukzhang"

# set token
RUN go env -w GOPROXY="https://vhukzhang:AdMjH8eW@goproxy.woa.com,direct" \
    && go env -w GOPRIVATE="" \
    && go env -w GOSUMDB="sum.woa.com+643d7a06+Ac5f5VOC4N8NUXdmhbm8pZSXIWfhek5JSmWdWrq7pLX4"

# cd /home/root/attribute_collection/ && ./attribute_collection 2>./panic_error.log &

