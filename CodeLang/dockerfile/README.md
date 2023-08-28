docker build -t dev_base:4 -f dockerfile/bsae.dockerfile .
docker run -it --name dev_envir_4 -v /data/home/vhukzhang/preci/remote/dev_envir:/root/dev_envir dev_base:4 /bin/bash
