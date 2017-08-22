#coding=utf-8
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码 

from bs4 import BeautifulSoup 


filename = 'result.html'
file = open(filename,'r', encoding='UTF-8')
web_data = file.read()
soup=BeautifulSoup(web_data,'lxml')# 解析网页 
#获取这个页面需要的信息
rows = soup.find_all('div', class_='newConversion')
for row in rows:
	print("写入成功：", end=' ')
	#print(list(row.stripped_strings))
	for x in row.contents:
		try:
			#print(x.attrs)
			if len(x.attrs['class']) > 1:
				if len(x.attrs['class'][1]) > 1:
					print(x.attrs['class'][1])
		except Exception as e:
			pass
	#for children in row.children:
	#	print(children.tag)
print ("完成")
