# 拉取基础镜像
FROM csighub.tencentyun.com/admin/tlinux2.2-bridge-tcloud-underlay:latest

# 作者信息
LABEL MAINTAINER="vhukzhang"

# 设置工作目录
WORKDIR /root

# 终端支持中文
ENV LANG=zh_CN.utf8

# 安装zsh
RUN sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)" \
    && cd ~/.oh-my-zsh/custom/plugins/ \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
    && git clone https://github.com/zsh-users/zsh-autosuggestions.git \
    && cd ~

# 安装go
ARG GO_VER=1.19.4
RUN wget https://go.dev/dl/go${GO_VER}.linux-amd64.tar.gz \
    && tar -C /usr/local -zxvf go${GO_VER}.linux-amd64.tar.gz \
    && rm go${GO_VER}.linux-amd64.tar.gz

# export env
ENV GO111MODULE=on
ENV GOPROXY=https://goproxy.woa.com/
ENV PATH=$PATH:/usr/local/go/bin:~/go/bin
RUN go env -w GOPROXY="https://vhukzhang:AdMjH8eW@goproxy.woa.com,direct" \
    && go env -w GOPRIVATE="" \
    && go env -w GOSUMDB="sum.woa.com+643d7a06+Ac5f5VOC4N8NUXdmhbm8pZSXIWfhek5JSmWdWrq7pLX4"

# init config
COPY vimrc /root/.vimrc
COPY init.sh /root/init.sh
RUN sh /root/init.sh

# go install
RUN go install git.code.oa.com/trpc-go/trpc-go-cmdline/trpc@latest

# crontab & start
RUN sed -i 's/required/sufficient/g' /etc/pam.d/crond \
    && echo "/usr/sbin/crond -n" >> /etc/kickStart.d/start_all.sh \
    && echo "/usr/local/services/AttaAgent-2.0/admin/restart.sh all" >> /etc/kickStart.d/start_all.sh
