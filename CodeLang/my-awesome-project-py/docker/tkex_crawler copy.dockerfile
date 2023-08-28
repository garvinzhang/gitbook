# 拉取基础镜像
FROM csighub.tencentyun.com/admin/tlinux2.2-bridge-tcloud-underlay:latest

# 作者信息
LABEL MAINTAINER="vhukzhang"

# 设置工作目录
WORKDIR /root

# 终端支持中文
ENV LANG=zh_CN.utf8

# 安装python3依赖
RUN yum -y update && yum -y upgrade \
    && yum -y groupinstall "Development Tools" \
    && yum -y install openssl-devel openssl bzip2-devel libffi-devel readline-devel \
    && yum -y install xz-devel sqlite-devel tk-devel db4-devel libpcap-devel snappy-devel \
    && yum -y install redis Xvfb xorg-x11-fonts*

# 安装python3
ARG PYTHON_VER=3.8.12
RUN wget https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tgz \
    && tar xvf Python-${PYTHON_VER}.tgz \
    && cd Python-${PYTHON_VER} \
    && ./configure --enable-optimizations \
    && make altinstall \
    && ln -s /usr/local/bin/python3.8 /usr/local/bin/python3 \
    && ln -s /usr/local/bin/python3.8-config /usr/local/bin/python3-config \
    && ln -s /usr/local/bin/pip3.8 /usr/local/bin/pip3 \
    && cd .. \
    && rm Python-${PYTHON_VER}.tgz \
    && rm -rf Python-${PYTHON_VER}

# 安装nodejs
ARG NODE_VER=v18.7.0
RUN wget https://nodejs.org/dist/${NODE_VER}/node-${NODE_VER}-linux-x64.tar.gz \
    && tar -C /usr/local --strip-components 1 -xzf node-${NODE_VER}-linux-x64.tar.gz \
    && rm node-${NODE_VER}-linux-x64.tar.gz

# 安装chrome的依赖
RUN yum -y groupinstall Fonts
RUN wget https://mirrors.tencent.com/centos/7.9.2009/os/x86_64/Packages/vulkan-1.1.97.0-1.el7.x86_64.rpm \
    && wget https://mirrors.tencent.com/centos/7.9.2009/os/x86_64/Packages/vulkan-filesystem-1.1.97.0-1.el7.noarch.rpm \
    && yum -y localinstall vulkan* \
    && rm vulkan*

# 安装chrome
ARG CHROME_VER=105.0.5195.52
RUN wget https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-${CHROME_VER}-1.x86_64.rpm \
    && yum -y localinstall google-chrome-stable-${CHROME_VER}-1.x86_64.rpm \
    && rm google-chrome-stable-${CHROME_VER}-1.x86_64.rpm

# 安装chromedrive
RUN wget https://npm.taobao.org/mirrors/chromedriver/${CHROME_VER}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && rm chromedriver_linux64.zip \
    && mv chromedriver ${ANACONDA_DIR}/bin/

# 安装zsh
RUN sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)" \
    && cd ~/.oh-my-zsh/custom/plugins/ \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
    && git clone https://github.com/zsh-users/zsh-autosuggestions.git \
    && cd ~

# GCC
COPY libstdc.so_.6.0.26.zip /root/libstdc.so_.6.0.26.zip
RUN cd /root \
    && unzip libstdc.so_.6.0.26.zip \
    && mv libstdc++.so.6.0.26 /usr/lib64/ \
    && rm /usr/lib64/libstdc++.so.6 \
    && ln -s /usr/lib64/libstdc++.so.6.0.26 /usr/lib64/libstdc++.so.6 \
    && cd /root

# 安装python3模块
RUN pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 install \
    black \
    protobuf attaapi aiohttp m007_metrics polaris-python \
    rainbow-sdk cos-python-sdk-v5 \
    pymysql redis kafka-python \
    requests pyyaml python_json_logger func_timeout \
    pytest pandas pillow opencv-python opencv-python-headless \
    scrapy scrapy_redis scrapy_splash \
    selenium selenium-stealth selenium-wire \
    pocoui airtest mitmproxy \
    tinydb tldextract django url_normalize \
    adblockparser chardet bs4 \
    --index-url https://mirrors.cloud.tencent.com/pypi/simple/ \
    --extra-index-url https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple/

#安装mitmproxy证书
RUN (mitmdump &) && sleep 2 \
    && cp .mitmproxy/mitmproxy-ca-cert.cer /etc/pki/ca-trust/source/anchors/mitmproxy-ca-cert.cer \
    && cp .mitmproxy/mitmproxy-ca-cert.cer /etc/pki/ca-trust/source/anchors/mitmproxy-ca-cert.crt \
    && update-ca-trust

# 安装 mongoDB
# RUN yum install -y mongodb-org

#添加adb执行路径&赋予权限
ENV PATH="/usr/local/lib/python3.8/site-packages/airtest/core/android/static/adb/linux:${PATH}"
RUN sh -c "chmod +777 /usr/local/lib/python3.8/site-packages/airtest/core/android/static/adb/linux/adb"

# init config
COPY vimrc /root/.vimrc
COPY init.sh /root/init.sh
RUN sh /root/init.sh

# crontab & start
RUN sed -i 's/required/sufficient/g' /etc/pam.d/crond \
    && echo "/usr/sbin/crond -n" >> /etc/kickStart.d/start_all.sh \
    && echo "/usr/local/services/AttaAgent-2.0/admin/restart.sh all" >> /etc/kickStart.d/start_all.sh
