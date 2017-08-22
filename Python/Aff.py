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

# 得到浏览器
#driver = webdriver.PhantomJS()
#本例中的网站仅支持Chrome
driver=webdriver.Chrome()

driver.get(r'https://app.afflow.rocks/')# 打开网页 
# 定位到输入框并输入
time.sleep(5)
inputUsername = driver.find_element_by_xpath (r'//*[@id="username"]')
inputPassword = driver.find_element_by_xpath (r'//*[@id="password"]')
inputUsername.send_keys(r"你的账号")
inputPassword.send_keys(r"你的密码")
# 提交 
submitElement = driver.find_element_by_xpath (r'//*[@id="keyEntryContainer"]/div/div/div[3]/input')
submitElement.click()
time.sleep(5)
# 输出网页标题
print (driver.title)

# 找到菜单
Menu = driver.find_element_by_xpath(r'//*[@id="menu_campaignsButton"]') 
# 鼠标悬停在菜单上
ActionChains(driver).move_to_element(Menu).perform()
# 查找并点击子菜单
liveLead = driver.find_element_by_xpath (r'//*[@id="menu_liveleadsButton"]')
liveLead.click()

filename = 'Aff_lead.csv'
csvfile = open(filename,'a')
writer = csv.writer(csvfile)

if not os.path.exists('Aff_lead.csv'):
	print('Aff_lead.csv not exist')
	item=['单价','转化时间','国家','类型','offerID','A/M']
	writer.writerow(item)

while True:
	time.sleep(3)
	web_data=driver.page_source		# 获取网页文件对象 
	#print (web_data)
	soup=BeautifulSoup(web_data,'lxml')# 解析网页 
	#获取这个页面需要的信息
	rows = soup.find_all('div', class_='newConversion')
	for row in rows:
		writer = csv.writer(csvfile,dialect='excel')
		writer.writerow(list(row.stripped_strings))
		print("写入成功：", end=' ')
		print(list(row.stripped_strings))

driver.quit()
csvfile.close()

print ("爬虫完成")
