# -*- coding:utf-8 -*-

#功能：文字转语音
#实现：调用百度测试语音api
#依赖：requests
#缺点：可能会不稳定，不知道百度语音api什么时候会挂


import sys
import os

if len(sys.argv) != 2:
    print ("useage:\n    python read.py " + "some world")
    print ("for example:\n    python read.py Hello World" )
    exit()

text = sys.argv[1]
url = 'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
          'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(text)
# 直接播放语音
os.system('mplayer "%s"' % url)
