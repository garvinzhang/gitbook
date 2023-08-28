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

# 安装go1.18.7
ARG GO_VER=1.18.7
RUN wget https://go.dev/dl/go${GO_VER}.linux-amd64.tar.gz \
    && tar -C /usr/local -zxvf go${GO_VER}.linux-amd64.tar.gz \
    && rm go${GO_VER}.linux-amd64.tar.gz

# mkdir 
RUN mkdir /root/go_project \
    && mkdir /root/go_path \
    && mkdir /root/go_path/src \
    && mkdir /root/go_path/bin \
    && mkdir /root/go_path/pkg

# export env
ENV GOROOT=/usr/local/go
ENV GO111MODULE=on
ENV GOPROXY=https://goproxy.cn
ENV GOPATH=/root/go_path
ENV PATH=$PATH:$GOROOT/bin:$GOPATH/bin

# init config
COPY vimrc /root/.vimrc
COPY init.sh /root/init.sh
RUN sh /root/init.sh

# crontab & start
RUN sed -i 's/required/sufficient/g' /etc/pam.d/crond \
    && echo "/usr/sbin/crond -n" >> /etc/kickStart.d/start_all.sh \
    && echo "/usr/local/services/AttaAgent-2.0/admin/restart.sh all" >> /etc/kickStart.d/start_all.sh
