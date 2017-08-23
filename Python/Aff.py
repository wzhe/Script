#coding=utf-8
import io
import sys
import time
import csv
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码 

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup 
from dateutil import parser

# 得到浏览器
#driver = webdriver.PhantomJS()
#本例中的网站仅支持Chrome
driver=webdriver.Chrome()

driver.get(r'https://app.afflow.rocks/')# 打开网页 
# 定位到输入框并输入
time.sleep(3)
inputUsername = driver.find_element_by_xpath (r'//*[@id="username"]')
inputPassword = driver.find_element_by_xpath (r'//*[@id="password"]')
inputUsername.send_keys(r"")
inputPassword.send_keys(r"")
# 提交 
submitElement = driver.find_element_by_xpath (r'//*[@id="keyEntryContainer"]/div/div/div[3]/input')
submitElement.click()
# 输出网页标题
print (driver.title)

# 找到菜单
time.sleep(5)
Menu = driver.find_element_by_xpath(r'//*[@id="menu_campaignsButton"]') 
# 鼠标悬停在菜单上
ActionChains(driver).move_to_element(Menu).perform()
# 查找并点击子菜单
liveLead = driver.find_element_by_xpath (r'//*[@id="menu_liveleadsButton"]')
liveLead.click()

filename = 'Aff_lead.csv'

exist_flag = False
if os.path.exists('Aff_lead.csv'):
    exist_flag = True

csvfile = open(filename,'a')
writer = csv.writer(csvfile)
if not exist_flag:
    print('Aff_lead.csv not exist')
    item=['单价','转化时间','国家与类型','offerID','A/M','os','browser']
    writer.writerow(item)

writer = csv.writer(csvfile,dialect='excel')
now = parser.parse('Aug 22nd, 22:56')
last = parser.parse('Aug 22nd, 22:56')

while True:
    time.sleep(3)
    print("-------now[%s]-------last[%s]-------",now,last)
    First = True 
    last = now
    web_data=driver.page_source     # 获取网页文件对象 
    #print (web_data)
    soup=BeautifulSoup(web_data,'lxml')# 解析网页 
    #获取这个页面需要的信息
    rows = soup.find_all('div', class_='newConversion')
    for row in rows:
        result = list(row.stripped_strings)
        for x in row.contents:
            try:
                if len(x.attrs['class']) > 1:
                    if len(x.attrs['class'][1]) > 1:
                        result.append(x.attrs['class'][1])
            except Exception as e:
                pass

        if(len(result) != 7):
            continue 
        if First:
            now = parser.parse(result[1])
            First = False
        if now == parser.parse(result[1]):
            continue
        if parser.parse(result[1]) > last:
            writer.writerow(result)
            print("写入成功：", end=' ')
            print(result)
    
driver.quit()
csvfile.close()

print ("完成")
