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
    && sed -i 's/robbyrussell/ys/' ~/.zshrc \
    && sed -i 's/plugins=(git)/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/' ~/.zshrc \
    && cd ~

# vim
RUN echo "syntax on" >> ~/.vimrc \
    && echo "set number" >> ~/.vimrc \
    && echo "set autoindent" >> ~/.vimrc \
    && echo "set expandtab" >> ~/.vimrc \
    && echo "set cursorline" >> ~/.vimrc \
    && echo "set ruler" >> ~/.vimrc \
    && echo "set hlsearch" >> ~/.vimrc

# crontab & start
RUN sed -i 's/required/sufficient/g' /etc/pam.d/crond \
    && echo "/usr/sbin/crond -n" >> /etc/kickStart.d/start_all.sh \
    && echo "/usr/local/services/AttaAgent-2.0/admin/restart.sh all" >> /etc/kickStart.d/start_all.sh
