#coding: utf-8
import sys
import urllib
import os
import requests
import threading
from urllib import request
from bs4 import BeautifulSoup
import socket
import time

TIME = 20                      # 单位是s
socket.setdefaulttimeout(TIME) # 设置延迟时间，请求超出时间就会断开



User_Agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Mozilla/4.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Mozilla/3.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Mozilla/2.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Mozilla/1.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.3112.78 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3112.78 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/23.0.3112.78 Safari/537.36']

#   print(int(time.time())%100)


class MyThread(threading.Thread):
    """
    属性:
    target: 传入外部函数, 用户线程调用
    args: 函数参数
    """
    def __init__(self, target, args):
        print("a new thread")
        super(MyThread, self).__init__()  #调用父类的构造函数 
        self.target = target
        self.args = args

    def run(self) :
        self.target(self.args)

def get_html(url_address):
    """
    通过url_address得到网页内容
    :param url_address: 请求的网页地址
    :return: html
    """
    headers = {'User-Agent':User_Agent[int(time.time())%len(User_Agent)],
               'Referer':'http://www.mzitu.com/',
               'Cookie':'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1503067509; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1503068270',
               'Connection':'keep-alive'}
    req = urllib.request.Request(url=url_address, headers=headers)
    calc = 0
    while(True):
        try:    
            ht = urllib.request.urlopen(req)
            break;
        except :
            print("获取网页超时！！！",calc);
            calc += 1
            if(calc == 20):
                ht = None
                print("网页获取失败！！！");
                break;
            time.sleep(20)
    return ht

#
def get_soup(html):
    """
    把网页内容封装到BeautifulSoup中并返回BeautifulSoup
    :param html: 网页内容
    :return:BeautifulSoup
    """
    if None == html:
        return
    return BeautifulSoup(html.read(), "html.parser")


def get_img_dirs(soup):
    """
    获取所有相册标题及链接
    :param soup: BeautifulSoup实例
    :return: 字典（ key:标题， value:内容）
    """
    if None == soup:
        return
    lis = soup.find(id="pins").findAll(name='li') # findAll(name='a') # attrs={'class':'lazy'}
    if None != lis:
        img_dirs = {};
        for li in lis:
            links = li.find('a')
            k = links.find('img').attrs['alt']
            t = links.attrs['href']
            img_dirs[k] = t;
        print(img_dirs)
        return img_dirs



def download_imgs(info):
    if None == info:
        return

    t = info[0]
    l = info[1]
    if None == t or None == l:
        return
    print("创建相册：" + t +" " + l)
    try:
        os.mkdir(t)
    except Exception as e:
        print("文件夹："+t+"，已经存在")

    print("开始获取相册《" + t + "》内，图片的数量...")

    dir_html = get_html(l)
    dir_soup = get_soup(dir_html)
    img_page_url = get_dir_img_page_url(l, dir_soup)
    
    # 得到当前相册的封面
    main_image = dir_soup.findAll(name='div', attrs={'class':'main-image'})
    
    if main_image != None:
        for image_parent in main_image:
            imgs = image_parent.findAll(name='img')
            #print ("###",imgs,"****")
            if None != imgs:
                img_url = str(imgs[0].attrs['src'])
                for i in range(len(img_page_url)+1):
                    ten = int((i+1) / 10)
                    one = int((i+1) % 10)
                    img_url = img_url[:-6] + str(ten) + str(one) + img_url[-4:]
                    filename = img_url.split('/')[-1]
                    print("开始下载:" + img_url + ", 保存为："+filename)
                    save_file(t, filename, img_url)

    # # 获取相册下的图片
    # for photo_web_url in img_page_url:
    #     download_img_from_page(t, photo_web_url)



def download_img_from_page(t, page_url):
    print("url is " + page_url)
    dir_html = get_html(page_url)
    dir_soup = get_soup(dir_html)

    # 得到当前页面的图片
    main_image = dir_soup.findAll(name='div', attrs={'class':'main-image'})
    if None != main_image:
        for image_parent in main_image:
            imgs = image_parent.findAll(name='img')
            if None != imgs:
                img_url = str(imgs[0].attrs['src'])
                filename = img_url.split('/')[-1]
                print("开始下载:" + img_url + ", 保存为："+filename)
                save_file(t, filename, img_url)


#http://i.meizitu.net/2017/02/01a04.jpg
def save_file(d, filename, img_url):
    headers = {'User-Agent':User_Agent[int(time.time())%len(User_Agent)],
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer':'http://www.mzitu.com/',#这是破解反爬虫的关键
               'Cookie':'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1503067509; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1503068270',
               'Connection':'keep-alive'}
    name = str(d+"/"+filename)
    if(os.path.exists(name)):
        print("已下载...")
        return
    calc = 0
    while(1):
        try :
            img = requests.get(url=img_url,timeout=TIME,headers=headers)
            break;
        except :
            print("下载图片超时！！！",calc,img_url);
            calc += 1
            if(calc == 20):
                print("图片获取失败！！！");
                return
            time.sleep(10)
    
    with open(name, "wb") as code:
        code.write(img.content)

def get_dir_img_page_url(l, dir_soup):
    """
    获取相册里面的图片数量
    :param l: 相册链接
    :param dir_soup:
    :return: 相册图片数量
    """
    divs = dir_soup.findAll(name='div', attrs={'class':'pagenavi'})
    navi = divs[0]
    code = navi['class']
    print(code)

    links = navi.findAll(name='a')
    if None == links:
        return
    a = []
    url_list = []
    for link in links:
        h = str(link['href'])
        n = h.replace(l+"/", "")
        try:
            a.append(int(n))
        except Exception as e:
            print(e)
    _max = max(a)
    for i in range(1, _max):
        u = str(l+"/"+str(i))
        url_list.append(u)
    return url_list

if __name__ == '__main__':
    parser = str(int(sys.argv[1]))      # 必须是数字
    url = 'http://www.mzitu.com/mm/page/'+parser
    print("开始解析：" + url)
    

    html = get_html(url)
    
    soup = get_soup(html)
    try:
        os.mkdir(parser)
    except Exception as e:
        print("文件夹："+parser+"，已经存在")
    os.chdir(parser)
    print(os.getcwd())

    img_dirs = get_img_dirs(soup)
    print (img_dirs)
    if None == img_dirs:
        print("无法获取该网页下的相册内容...")
    else:
        for d in img_dirs:
            my_thread = MyThread(download_imgs, (d, img_dirs.get(d)))
            my_thread.start()
            #my_thread.join()
    print("end!")
#    #save_file("a","b.jpg",'http://i.meizitu.net/2017/02/01a04.jpg')

