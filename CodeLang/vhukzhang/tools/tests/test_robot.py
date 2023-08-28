#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR)

from tools.tests.test_init import INIT_ALL, GetFastLog

test_log = GetFastLog(__file__)



mentionedList = ["vhukzhang", "@all"]
# mentionedList = ["@all"]
# mentionedList = ["vhukzhang"]
INIT_ALL.QYWX_ROBOT.SendMsg(
    content="test",
    msgType="text",
    mentionedList=mentionedList,
)

# 实际上展示的效果是 就title1和2的大小是比加粗字体大的，所以一般使用title1和2就可以
content = "\
# title1 \n\
## title2 \n\
### title3 \n\
#### title4 \n\
##### title5 \n\
###### title6 \n\
\n\
**bold**\n\
\n\
[This is a link](https://www.qq.com/) \n\
\n\
`code` \n\
\n\
> 引用 \n\
\n\
<font color='info'>green</font> \n\
<font color='comment'>gray</font> \n\
<font color='warning'>orange</font> \
"
ok, err = INIT_ALL.QYWX_ROBOT.SendMsg(
    content=content,
    msgType="markdown",
    mentionedList=mentionedList,
)
test_log.info(ok)
test_log.info(err)
