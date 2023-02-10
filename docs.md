# ALL IN ONE

## Linux Util

### Base

#### VIM

```vimrc
" 语法高亮
syntax on
" 显示行号
set number
" 自动缩进
set autoindent
" 缩进的tab转换成空格
set expandtab
" 当前行高亮
set cursorline
" 显示光标的位置
set ruler
" 高亮搜索显示
set hlsearch
```

#### ZSH

```zsh
# 安装ZSH
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)" \
    && cd ~/.oh-my-zsh/custom/plugins/ \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
    && git clone https://github.com/zsh-users/zsh-autosuggestions.git \
    && cd ~

# 配置zsh
sed -i 's/robbyrussell/ys/' ~/.zshrc
sed -i 's/plugins=(git)/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/' ~/.zshrc
```

#### ALIAS

```bash
# 自定义命令
vim ~/.bashrc
alias vim="nvim"
alias python="/src/bin/python3"
```

#### PS & GREP

```bash
# 通过进程名称关闭进程
ps ax | grep 'main.py' | grep -v grep | awk '{print $1}' | xargs kill
# TKEx平台的进程存活监测
ps -ef | grep main.py | grep -v grep

# 基于特定后缀文件的查找
grep -r "insert into" *.py
```

#### ZIP & TAR

```bash
# 压缩
zip abc.zip abc.file  # 压缩一个文件
zip test.zip install.log install.log.syslog  # 压缩多个文件
zip -r dir.zip dir/  # 压缩文件夹

# 解压缩 文件名乱码问题
unzip -O cp936 xxx.zip
```

#### SHELL 切换 root 用户

```bash
su root

export RootPWD="xxxxx"
echo $RootPWD
```

### Git

#### 免密登陆

```bash
# 查看git配置
git config --list
# 设置密码保存
git config --global credential.helper store
# 首次使用需要输入密码
git config --global user.email "xxx@xxx.com"
git config --global user.name "xxx"
```

#### 提交规范

| 提交标签 | 意义                                              |
| :------- | ------------------------------------------------- |
| feat     | 新功能（feature）                                 |
| fix      | 修补 bug                                          |
| docs     | 文档（documentation）                             |
| style    | 格式（不影响代码运行的变动）                      |
| refactor | 重构（即不是新增功能，也不是修改 bug 的代码变动） |
| test     | 增加测试                                          |
| chore    | 构建过程或辅助工具的变动                          |

#### 子模块

```bash
# 为项目添加子模块 - 模拟器采集框架子模块
git submodule add https://xxx.git
# 克隆项目时同时克隆项目的子模块
git clone --recursive https://xxx.git
# 更新所有的子模块
git submodule update --remote
```

### Docker

#### 构建镜像和挂载容器

```bash
# 基于dockerfile构建镜像
docker build -t {ImageNAME}:{TAG} -f Dockerfile .

# {LocalPATH}和{ContainerPATH}需要是绝对路径
docker run -it --name {ContainerNAME} -v {LocalPATH}:{ContainerPATH} {ImageNAME}:{TAG} /bin/bash
```

#### 启动、关闭容器

```bash
docker start ${ContainerNAME}
docker stop ${ContainerNAME}
```

#### 普通用户 权限问题

```bash
# 在rootUser执行
su
gpasswd -a normalUser docker
```

## Code Lang

### Python

#### 虚拟环境

```bash
# 创建虚拟环境
python3 -m venv ~/PyVenv/test_env

# 进入虚拟环境
source ~/PyVenv/test_env/bin/activate

# 退出虚拟环境
deactivate
```

#### 后台运行

```bash
# 日志默认可以实时写入
nohup python3 main.py >> nohup.out &

# print的实时写入
nohup python3 -u main.py >> nohup.out &
```

#### 依赖文件

```bash
# 生成依赖文件
pipreqs ./
# 强制覆盖生成新的依赖文件
pipreqs --force ./

# 安装依赖文件
pip3 install -r ./requirements.txt \
    --index-url https://mirrors.cloud.tencent.com/pypi/simple/ \
    --extra-index-url https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple/
```

#### 文本解码

```python
# 将"\xE5\xB9\xB3\xE5\xAE..."转为中文
start_data = "\xE5\xB9\xB3\xE5\xAE\x89\xE9\x93\xB6\xE8\xA1\x8C\xE8\x82\xA1\xE4\xBB\xBD\xE6\x9C\x89\xE9\x99\x90\xE5\x85\xAC\xE5\x8F\xB8\xE6\xB7\xB1\xE5\x9C\xB3\xE5\x88\x86\xE8\xA1\x8C"
first_data = start_data.encode("raw_unicode_escape")
last_data = first_data.decode()
print(last_data)
# 平安银行股份有限公司深圳分行
```

#### Json 字典 字符串

```python
# Json 字典
import json
info_map = {"a": 1, "b": "hello"}
info_map_str = json.dumps(info_map)
print(type(info_map_str))
info_map = json.loads(info_map_str)
print(type(info_map))

# 字典 字符串
import ast
one_dict = {"a": 1, "b": "hello"}
one_str = str(one_dict)
demo_dict = ast.literal_eval(one_str)
demo_dict == one_dict
```

### Go

#### 环境安装

```bash
# 切换到root用户
# 下载 Go 源码包，请保证下面的版本号是较新的
wget https://go.dev/dl/go1.19.linux-amd64.tar.gz
# 移除旧的已有安装，并解压出新的安装（需要 root 权限）
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz

# vim ~/.bashrc
# 至于这里为什么这么配置, 可参考 https://learnku.com/go/t/39086#0b3da8
export GO111MODULE=on
# 请点击以下链接, 进行设置go proxy和go sumdb:
https://goproxy.woa.com/
# 把go命令以及gopath添加到path环境变量
export PATH=$PATH:/usr/local/go/bin:~/go/bin

# go install git.code.oa.com/trpc-go/trpc-go-cmdline/trpc@latest
```

## Data Table

### Redis

#### Util

```bash
# 设置此db的使用方
select [db]
set owner 'the use of this db'

# 查看所有的key
dbsize
keys *

# 删除所有的key
flushdb
flushall

# 查看列表key的长度
llen key
```

### Mysql

#### 创建数据表模版

```sql
-- Template
id int(8) NOT NULL AUTO_INCREMENT COMMENT '自增计数',
 int(8) NOT NULL DEFAULT 0 COMMENT '',
 float NOT NULL DEFAULT 0 COMMENT '',
 varchar(64) NOT NULL DEFAULT '' COMMENT '',
 text COMMENT '',
date_ds int(4) NOT NULL DEFAULT 20010101 COMMENT '数据写入日期分区ds',
insert_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (id,date_ds),
index (insert_time)
```

#### 增删改查

```sql
-- 获取字段的后几位
select SUBSTRING(userLink, -3) from db.table;

-- 增加 更新 删除
INSERT into db.table (account) values ("test_unique");
UPDATE db.table SET FirstName = 'Fred' WHERE LastName = 'Wilson';
DELETE FROM db.table WHERE FirstName = 'Fred';
```

### Hive

### Mongo

### Kafka

