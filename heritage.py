#encoding=utf-8

import urllib
import urllib2
import time 
import sys
from bs4 import BeautifulSoup
import json
import socket
import ssl
import os 
import random

ssl._create_default_https_context = ssl._create_unverified_context

#设置系统编码格式
reload(sys)
sys.setdefaultencoding('utf-8')

def processing_str(html , save_path):
	"""
		作用：处理字符串中多余的转义字符，并将他们以字典的形式存储;
		@html:open_url()返回的html文件;
		@save_path:文本保存的路径;
	"""
	soup = BeautifulSoup(html)
	title = str(soup.find('div' , id = 'title').get_text()).replace(" " , "").replace("\n" , "").replace("\t" , "").replace("\r" , "")
	year = str(soup.find('td' , id = 'shijian').get_text()).replace(" " , "").replace("\n" , "").replace("\t" , "").replace("\r" , "")
	classfication = str(soup.find('td' , id = 'leibie').get_text()).replace(" " , "").replace("\n" , "").replace("\t" , "").replace("\r" , "")
	area = str(soup.find('td' , id = 'diqu').get_text()).replace(" " , "").replace("\n" , "").replace("\t" , "").replace("\r" , "")
	number = str(soup.find('td' , id = 'bianhao').get_text()).replace(" " , "").replace("\n" , "").replace("\t" , "").replace("\r" , "")
	content = str(soup.find('div' , id = 'jianjie').get_text()).replace("\n" , "").replace("\t" , "").replace("\r" , "")

	file_dic = {
		'title' : title,
		'year' : year,
		'classfication' : classfication, 
		'area' : area,
		'number' : number,
		'content' : content,
	}
	save_txt(file_dic , save_path , classfication , title)

def handling_Exceptions(request):
	"""
		作用：处理异常；
	"""
	try:
		html = urllib2.urlopen(request).read().decode('utf-8')
	except (urllib2.HTTPError, socket.error):
		if urllib2.HTTPError:
			print "HTTPError"
			return 0
		if socket.error:
			print "timeout"
			time.sleep(20)
			handling_Exceptions(request)
	else:	
		return html

def open_url(url):
	"""
		作用:打开国家级非物质文化遗产名录的url；
		@url:国家级非物质文化遗产名录的url；
	"""
	headers = {
		"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		#请求报头域，用于指定客户端接受哪些信息
		"Accept-Language" : "zh-CN,zh;q=0.9",
		#（目测是）对页面的语言选择
		"Cache-Control" : "max-age=0",
		#用于指定缓存指令，缓存指令是单向、独立的
		"Cookie" : "_pk_ref.1.d89e=%5B%22%22%2C%22%22%2C1544005681%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dd8dQSvDDqgwPYuhlYWzWYL0UYdw7AUQb3--8HrxFxcm%26wd%3D%26eqid%3Da6a29f4d0084a85d000000025c07a829%22%5D; _pk_ses.1.d89e=*; _pk_id.1.d89e=ad25f69289f13466.1544005681.1.1544009581.1544005681.",

		"Host" : "www.ihchina.cn",
		#用于指定请求资源的Internet主机和端口号，必须表示请求URL的原始服务
		#器或网关的位置

		# "If-Modified-Since" : "Tue, 21 Aug 2018 06:25:24 GMT",
		# "If-None-Match" : 'W/"5b7bb054-35ea"',
		"Proxy-Connection" : "keep-alive",

		"Referer" : "http://www.ihchina.cn/5/5_1.html",
		# 对付“反盗链”(服务器会识别headers中的referer是不是它自己,如果不是则不响应)
		"Upgrade-Insecure-Requests" : "1",

		"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
		#User-Agent用于辨别浏览器身份，伪装自己的爬虫身份以防止服务器拒绝爬虫访问
	}


	request = urllib2.Request(url , headers = headers)
	html = handling_Exceptions(request)
	return html

def save_txt(file_dic , sava_path , classfication , title):
	"""
		作用:保存文件
		@file_dic:需要保存的信息;
		@save_path:保存的路径;
		@classfication:文件的类别;
		@title:文件的名字;
	"""
	json_str = json.dumps(file_dic , ensure_ascii=False)
	path = save_path + classfication
	json_path = path + "/" + title + ".json"
	final_path = json_path

	#判断当前路径是否存以需要保存的文本的类别命名的文件夹
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
		print "已创建" + classfication + "文件夹"
	#处理文件名过长无法保存的异常
	try :
		json_file = open(final_path , 'a') 
	except IOError:
		print IOError
		title = title[0 : 20]
		print title
		json_path = path + "/" + title + ".json"
		final_path = json_path
		json_file = open(final_path , 'a') 
		json_file.write(json_str)
		print title + "下载成功"
	else:
		json_file.write(json_str)
		print title + "下载成功"

def spider(url , save_path):
	"""
		作用:
		@url:
	"""
	key = 10618
	while key:
		final_url = url + str(key) + '.html'
		html = open_url(final_url)
		if html == 0:
			print "下载结束"
			return 
		else:
			file_dic = processing_str(html , save_path)
			# time.sleep(random.randint(1 , 3))
			key = key + 1

if __name__== "__main__":
	"""
		作用:主函数;
	"""
	url = "http://www.ihchina.cn/5/"
	save_path = "new"
	spider(url , save_path)