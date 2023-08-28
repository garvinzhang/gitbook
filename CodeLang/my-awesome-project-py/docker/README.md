# docker 镜像构建

`docker build -t tkex:crawler_01 -f docker/tkex_crawler.dockerfile .`

`docker build -t vhukzhang:tkex_crawler_02 -f docker/tkex_crawler.dockerfile .`

`docker run -i -t --name vhukzhang_tkex_crawler_04 vhukzhang:tkex_crawler_04 /bin/bash`
