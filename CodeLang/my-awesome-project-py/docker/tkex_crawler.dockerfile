# 拉取基础镜像
FROM csighub.tencentyun.com/admin/tlinux2.2-bridge-tcloud-underlay:latest

# 作者信息
LABEL MAINTAINER="vhukzhang"

# 设置工作目录
WORKDIR /usr/local/app

# 终端支持中文
ENV LANG=zh_CN.utf8
ENV PATH=/opt/conda/bin:$PATH

# 安装conda环境
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && conda create --name conda39 python=3.9 -y \
    && conda init \
    && echo "conda activate conda39" >> ~/.bashrc

# 配置vim
RUN echo "set number" >> ~/.vimrc \
    && echo "syntax on" >> ~/.vimrc \
    && echo "set showmode" >> ~/.vimrc \
    && echo "set encoding=utf-8" >> ~/.vimrc \
    && echo "set autoindent" >> ~/.vimrc \
    && echo "set expandtab" >> ~/.vimrc \
    && echo "set relativenumber" >> ~/.vimrc \
    && echo "set cursorline" >> ~/.vimrc \
    && echo "set ruler" >> ~/.vimrc \
    && echo "set showmatch" >> ~/.vimrc \
    && echo "set hlsearch" >> ~/.vimrc \
    && echo "set visualbell" >> ~/.vimrc \
    && echo "set autoread" >> ~/.vimrc

# 安装python包
RUN source ~/.bashrc \
    && pip install \
    requests 
