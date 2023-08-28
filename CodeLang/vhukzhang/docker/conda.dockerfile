# 拉取基础镜像
FROM csighub.tencentyun.com/vhukzhang/vhukzhang:alpine1

# 作者信息
LABEL MAINTAINER="vhukzhang"

# 设置工作目录
WORKDIR /root

# 安装依赖
RUN yum -y install epel-release git-lfs \
    gcc gcc-c++ make openssl-devel \
    bzip2-devel libffi-devel zlib-devel \
    swig

# 安装cmake
RUN wget https://cmake.org/files/v3.12/cmake-3.12.4.tar.gz \
    && tar -xzvf cmake-3.12.4.tar.gz \
    && cd cmake-3.12.4 \
    && ./bootstrap && make && make install

# 安装conda环境 @TODO
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh
ENV PATH /opt/conda/bin:$PATH
RUN conda create --name conda38 python=3.8 -y \
    && echo "conda activate conda38" >> ~/.bashrc \
    && conda config --set auto_activate_base false
# RUN pip install requests

RUN && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && sh Miniconda3-latest-Linux-x86_64.sh -b \
    && conda create --name conda38 python=3.8 -y \
    && conda activate conda38 \
    && rm Miniconda3-latest-Linux-x86_64.sh



# docker build -t conda:01 -f docker/conda.dockerfile .

# git
RUN git config --list \
    && git config --global credential.helper store \
    && git config --global user.email "vhukzhang@tencent.com" \
    && git config --global user.name "vhukzhang" \
    && git config --list

# wget https://git.woa.com/vhukzhang/vhukzhang/raw/develop/tmp/file/private_key.dat
cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON3_INTERFACE=ON ..
make -j
python3 examples/py3/wordseg_example.py /root/qqseg/data/
python3 examples/py3/func_qqseq.py /root/qqseg/data/

sudo sysctl -w vm.overcommit_memory=1
sudo sysctl -w vm.overcommit_ratio=100

sudo sysctl -w vm.overcommit_memory=2
sudo sysctl -w vm.overcommit_ratio=0
