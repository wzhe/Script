#coding=utf-8
 2 import urllib
 3 import urllib2
 4 import re
 5 import os
 6 
 7 webroot = 'http://www.xuanshu.com'
 8 
 9 for page in range(20,220):
     print '正在下载第'+str(page)+'页小说'
     
     url = 'http://www.xuanshu.com/soft/sort02/index_'+str(page)+'.html'
     headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }
     try:
         request = urllib2.Request(url,headers=headers)
         response = urllib2.urlopen(request,timeout=180)
         #print response.read()
     except urllib2.URLError, e:
         if hasattr(e,"code"):
             print e.code
         if hasattr(e,"reason"):
             print e.reason
 
     html = response.read().decode('utf-8')
     #print html
     pattern = re.compile(u'<li>.*?<div class="s">.*?target="_blank">(.*?)</a><br />大小：(.*?)<br>.*?</em><br>更新：(.*?)</div>.*?<a href="(.*?)"><img.*?>(.*?)</a>.*?<div class="u">(.*?)</div>',re.S)
     items = re.findall(pattern,html)
     #print items
 
     for item in items:
         try:
             book_auther = item[0].encode('gbk')
             book_size = item[1].encode('gbk')
             book_updatetime = item[2].encode('gbk')
             book_link = item[3].encode('gbk')
             book_name = item[4].encode('gbk')
             book_note = item[5].encode('gbk')
             
             book_full_link = webroot + book_link    # 构建书的绝对地址
 
             #请求地址
             try:
                 request = urllib2.Request(book_full_link,headers=headers)
                 response = urllib2.urlopen(request,timeout=180)
             except urllib2.URLError, e:
                 if hasattr(e,"code"):
                     print e.code
                 if hasattr(e,"reason"):
                     print e.reason
             html = response.read().decode('utf-8')
             #print html
             pattern = re.compile('<a class="downButton.*?<a class="downButton" href=\'(.*?)\'.*?Txt.*?</a>',re.S)
             down_link = re.findall(pattern,html)
             print book_name
             print down_link
             
             # down txt
             try:
                 request = urllib2.Request(down_link[0].encode('utf-8'),headers=headers)
                 response = urllib2.urlopen(request,timeout=180)
             except urllib2.URLError, e:
                 if hasattr(e,"code"):
                     print e.code
                 if hasattr(e,"reason"):
                     print e.reason
             try:
                 fp = open(book_name+'.txt','w')
             except IOError,e:
                 pattern = re.compile('<strong>.*?>(.*?)<.*?</strong>',re.S)
                 book_name = re.findall(pattern,book_name)
                 fp = open(book_name[0]+'.txt','w')
             print 'start download'
             fp.write(response.read())
             print 'down finish\n'
             fp.close()
         except Exception,e:
             print '该条目解析出现错误，忽略'
             print e
             print ''
             fp = open('error.log','a')
             fp.write('page:'+str(page)+'\n')
             fp.write(item[4].encode('gbk'))
             #fp.write(e)
             fp.write('\nThere is an error in parsing process.\n\n')
             fp.close()
         
         
