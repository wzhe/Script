# -*- coding:utf-8 -*-

#功能：文字转语音
#实现：调用百度测试语音api
#依赖：requests
#缺点：可能会不稳定，不知道百度语音api什么时候会挂


import sys

if len(sys.argv) != 3:
    print ("useage:\n    python read.py " + "some world + audiofilename(without mp3)")
    print ("for example:\n    python read.py \"Hello World\" He")
    exit()

import requests

text = sys.argv[1]
audoFileName = sys.argv[2]+".mp3"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
    
url = 'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
      'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(text)
res = requests.get(url, headers=headers)
with open(audoFileName, 'wb') as f:
    f.write(res.content)
