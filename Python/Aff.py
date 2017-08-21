#coding=utf-8
 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup 
import time
driver=webdriver.Chrome()# 得到浏览器 
driver.get(r'https://app.afflow.rocks/')# 打开网页 
# 定位到输入框并输入
time.sleep(5)
inputUsername = driver.find_element_by_xpath (r'//*[@id="username"]')
inputPassword = driver.find_element_by_xpath (r'//*[@id="password"]')
inputUsername.send_keys(r"你的帐号")
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

web_data=driver.page_source		# 获取网页文件对象 
#print (web_data)


soup=BeautifulSoup(web_data,'lxml')# 解析网页 
#获取这个页面需要的信息
rows = soup.find_all('newConversion')
row_data =	list(rows.stripped_strings)
print(row_data)

print ("爬虫完成")


'''
# encoding=utf-8  
from selenium import webdriver  
from selenium.webdriver.common.action_chains import ActionChains  
  
browser = webdriver.Chrome('E:\\chromedriver.exe')  
browser.maximize_window()  
browser.get('http://www.uestc.edu.cn/')  
# 方法一：使用find_element_by_link_text找到顶级菜单，并将鼠标移动到上面  
article = browser.find_element_by_link_text(u'学校概况')  
ActionChains(browser).move_to_element(article).perform()  
# 方法二：使用find_element_by_xpath找到顶级菜单，并将鼠标移动到上面  
# article = browser.find_element_by_xpath('//a[contains(@href,"?ch/3")]')  
# ActionChains(browser).move_to_element(article).perform()  
# 方法一：使用find_element_by_link_text找到二级菜单，并点击  
# menu = browser.find_element_by_link_text(u'学校简介')  
# 方法二：使用find_element_by_xpath找到二级菜单，并点击  
menu = browser.find_element_by_xpath('//li[@classes="first odd nth1"]')  
menu.click()  
'''