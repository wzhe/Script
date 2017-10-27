# -*- coding: utf-8 -*-
import urllib
import re
import sys
import requests
#reload(sys)
#sys.setdefaultencoding('utf8')

SLUG = "readhub"
WORDS = ["XINWEN"]

DEFAULT_ROW = 10
DEFAULT_DETAIL = False


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
def getHtml():
    url = 'https://readhub.me/'
    html = ""
    try:
        response = requests.get(url, headers=headers)
        html = response.text
    except :
        print("Error open readhub")
    return html

def handleHtml(html):
    detail = DEFAULT_DETAIL
    row = DEFAULT_ROW
    if SLUG in profile :
        if 'row' in profile[SLUG]:
            row = profile[SLUG]['row']
        if 'detail' in profile[SLUG]:
            detail = profile[SLUG]['detail']
    patten = re.compile('<span class="content___2vSS6">(.*?)</span>', re.S)
    results = re.findall(patten, html)
    if (detail):
        patten_detail = re.compile('<div class="summary___1i4y3">(.*?)</div>', re.S)
        results_detail = re.findall(patten_detail, html)
    news = ""
    num = 1;
    for i in results:
        if (num <= row):
            news += str(num) + ' '+ i + '\n'
            if (detail):
                news += results_detail[num-1] + '\n'
            num += 1
        else:
            break
    return news


def handle(text, mic, profile, wxbot=None):
    html = getHtml()
    if html:
        news = handleHtml(html)
        if news:
            mic.say(news)
        else:
            mic.say(u"新闻解析有误 请重试")
    else:
        mic.say(u"网络连接有误 请重试")

def isValid(text):
    return u"新闻" in text
def main():
    html = getHtml()
    str = handleHtml(html)
    print(str)

if __name__ == '__main__':
    main()