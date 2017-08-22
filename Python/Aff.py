#coding=utf-8
import io
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup 
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码 
driver=webdriver.Chrome()# 得到浏览器 
driver.get(r'https://app.afflow.rocks/')# 打开网页 
# 定位到输入框并输入
time.sleep(5)
inputUsername = driver.find_element_by_xpath (r'//*[@id="username"]')
inputPassword = driver.find_element_by_xpath (r'//*[@id="password"]')
inputUsername.send_keys(r"linuxmintnot@gmail.com")
inputPassword.send_keys(r"3n7s9XkpCa")
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

time.sleep(3)
web_data=driver.page_source		# 获取网页文件对象 
#print (web_data)


soup=BeautifulSoup(web_data,'lxml')# 解析网页 
#获取这个页面需要的信息
rows = soup.find_all('div', class_='newConversion')
for row in rows:
	print(row.span.strings)

while False:
	new_data_page = driver.page_source		# 获取网页文件对象
	soup_newdata = BeautifulSoup(new_data_page,'lxml')# 解析网页
	new_data = soup.find_all('div', class_='newConversion')


soup=BeautifulSoup(web_data,'lxml')# 解析网页 

print ("爬虫完成")
