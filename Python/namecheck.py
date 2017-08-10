#!/usr/bin/python
# -*- coding: utf-8 -*-


##########################################################################
#Author 王哲
#Auto check the comian name is expired
##########################################################################
#域名       注册时间        到期时间        状态
#google.com 2001/03/02      2018/10/10       -
#007city.com    -               -            OK
#
##########################################################################
import sys
import urllib2
from bs4 import BeautifulSoup
import csv
import time
import random
import json
import requests 

import codecs

codes =['519983','002529','/02318','/SZ000001','/SH510900','/SZ168101']

filename = 'result_miss.csv'

reload(sys)
sys.setdefaultencoding('utf-8')


#wget -c http://s3.amazonaws.com/alexa-static/top-1m.csv.zip
all_IP = [["118.99.36.15", 808, 0], ["122.142.77.84", 80, 0]]
def re_get_proxy():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=10') 
    global all_IP
    all_IP = json.loads(r.text) 
    #print all_IP
    #print type(all_IP)
def open_url(url):
    ip = random.choice(all_IP)
    #print ip
    proxy_ip = "http://" + ip[0] + ":" + str(ip[1])
    print proxy_ip
    global request_headers


    proxy_support = urllib2.ProxyHandler({'http':proxy_ip})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

#def open_url(url):
    request_headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"utf-8",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Host":"typo.namewest.com",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }
    print "start connect " + url
    req = urllib2.Request(url, headers=request_headers)
    try:
        response = urllib2.urlopen(req,timeout=8).read()
    except:
        print "connect fail!"
        return
    print "connect success!"
    soup = BeautifulSoup(response, "html.parser")
    #print soup
    return soup

def get_all_typo_name(name):
    typo_url = "http://typo.namewest.com/?q=" + name +"&missed=on&swap=on&hwrong=on&double=on&alike=on"
    soup = open_url(typo_url)
    if (not soup):
        return []
    #print soup
    #all_typo = soup.find_all(name="textarea",class_="form-control")
    all_typo = soup.find_all("div",role="typolist")
    count = 0
    print "-------------------------------------------------"
    print all_typo
    print "_________________________________________________"
    for child in all_typo[0].children:
        count += 1
        if(count <= 2):
            #print "--" + child.string + "0-0"
            continue 
        if (len(child.string) == 1):
            continue
        all_typo_name = child.string.split()
        return all_typo_name
        #for typo_name in all_typo_name:
        #    print typo_name
def check_domain_state(domain):
    now = str(int(time.time()))
    state_url = "http://typo.namewest.com/check_status.php?domain=" + domain + "&timestamp=" + now
    soup = open_url(state_url)
    domain_state=[domain,"-","-","-"]
    if (not soup):
        return domain_state
    
    print domain 
    state_ok = True
    for years_string in soup.strings:
        #print years_string
        years = years_string.split("/",1)
        if(len(years) == 2 ):
            if(len(years[0]) > 0):
                domain_state[1] = years[0].strip().split()[0]
                domain_state[2] = years[1].strip().split()[0]
            else:
                domain_state[3] = years[1].strip()
                break;
            if(len(years[1].strip().split()) == 2):
                domain_state[3] = years[1].strip().split()[1]
            if(len(years[1].strip().split()) == 3):
                domain_state[3] = years[1].strip().split()[1] +  years[1].strip().split()[2] 
            state_ok = False
    if (state_ok):
        domain_state[3] = "OK"
    return domain_state

def write_result(csvfile,domain_state):
    domain = domain_state[0]
    start_date = domain_state[1]
    end_date = domain_state[2]
    state = domain_state[3]
    result =  'domain:' + domain + ' start_date:'+ start_date + ' end_date:' + end_date +  '  state:' + state
    item=[domain,start_date,end_date,state]
    writer = csv.writer(csvfile,dialect='excel')
    writer.writerow(item)
    print '写入成功   结果为:  ' + result

def write_all_result(all_result):
    csvfile = open(filename,'ab')
    csvfile.write(codecs.BOM_UTF8)
    for domain_state in all_result:
        write_result(csvfile,domain_state)
    csvfile.close()

def write_fail_result(domain):
    csvfile = open("failname.txt",'ab')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile,dialect='excel')
    writer.writerow(domain)
    csvfile.close()

def main():
    item=['域名','注册时间','到期时间','状态']
    csvfile = open(filename,'ab')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    writer.writerow(item)
    csvfile.close()
    
    f = open("top_10000.txt", "r")  
    time_count = 0;
    while True:  
        line = f.readline()  
        if line:  
            if(time_count%20 == 0):
                re_get_proxy()
            time_count += 1
            all_typo_name = get_all_typo_name(line.strip())
            if(len(all_typo_name) == 0):
                write_fail_result(line.strip())
                continue
            all_result = []
            all_result.append(check_domain_state(line.strip()))
            for typo_name in all_typo_name:
                all_result.append(check_domain_state(typo_name))
                #time.sleep(0.01)
            write_all_result(all_result)
            #time.sleep(1)
        else:  
            break  
    f.close()  


if __name__ =="__main__":
    main()
                   
