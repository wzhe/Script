#coding=utf-8
 
from selenium import webdriver
from bs4 import BeautifulSoup 

driver=webdriver.Chrome()# 得到浏览器 
driver.get(r'http://zhaosheng.cdce.cn/ShowProfession.aspx?code=10001')# 打开网页 
while True:
	web_data=driver.page_source# 获取网页文件对象 
	soup=BeautifulSoup(web_data,'lxml')# 解析网页 
	#获取这个页面需要的信息
	rows = soup.find_all('table', width="950",align="center")
	row = rows[-1]
	row_data =list(row.stripped_strings)
	row_data = row_data[5:]
	all_page = 0
	current_page = 0

	for x in range(1,18):
		if 16 == x:
			current_page = int(row_data.pop())
		elif 14 == x:
			all_page = int(row_data.pop())
		else:
			row_data.pop()
	print(row_data)	
	print(all_page)
	print(current_page)
	#此页信息采集，开始继续采集下一页信息 
	if current_page < all_page:
		driver.find_element_by_xpath(r'//*[@id="ctl00_ContentPlaceHolder1_PlanControl1_btnNext"]').click()#采用chrome浏览器粘贴下一页这个键的xpath定位，并点击 	
		##chrome浏览器复制得到的下一页按钮 
		#//*[@id="ctl00_ContentPlaceHolder1_PlanControl1_btnNext"]
	else:
		break

print ("爬虫完成")