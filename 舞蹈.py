#encoding=utf-8

import urllib2
import urllib
import json
import re
import zlib
import time
import socket 

def serch_Key(serch_url, keyword, page):
	"""
		作用：根据关键字搜索相关视频，解析json文件，返回播放相关视频的url
		@keyword: 视频的关键字
		@play_url：视频的播放地址
	"""
	data = {
		"page" : page,
		"callback" : "__jp0",
		"from_source" : "banner_search",
		"keyword" : keyword,
		"highlight" : "1",
		"jsonp" : "jsonp"
	}
	data = urllib.urlencode(data)

	headers ={
		"Host" : "api.bilibili.com",
		"Connection" : "keep-alive",
		"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
		"Accept" : "*/*",
		"Referer" : "https://search.bilibili.com/all?" + urllib.urlencode({"keyword" : keyword}),
		"Accept-Language" : "zh-CN,zh;q=0.9",
	}

	request = urllib2.Request(serch_url + data, headers = headers)
	result = urllib2.urlopen(request).read().decode("utf-8")
	result = result[6:(len(result)-1)]

	#解析服务器返回的json文件
	data_dict = json.loads(result)
	dic = data_dict['data']['result']['video']

	# 将我们需要的信息存到下列列表当中
	tag = []
	author = []
	description = []
	title = []
	play_url = []
	for i in range (len(dic)):
		tag.append(dic[i]['tag'])
		author.append(dic[i]['author'])
		description.append(dic[i]['description'])
		title.append(dic[i]['title'])
		play_url.append(dic[i]['arcurl'])

	return tag, author, description, title, play_url
	
def open_Movie(play_url, title):
	"""
		作用：打开一个视频的url，解析html文件，返回视频的下载地址
		@play_url：播放视频的地址
		@down_url：视频的下载地址
	"""
	headers = {
		"Host" : "www.bilibili.com",
		"Connection" : "keep-alive",
		"Cache-Control" : "max-age=0",
		"Upgrade-Insecure-Requests" : "1",
		"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
		"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding" : "gzip, deflate, br",
		"Accept-Language" : "zh-CN,zh;q=0.9"
	}

	request = urllib2.Request(play_url, headers = headers)
	html = urllib2.urlopen(request).read()
	decompressed_data = zlib.decompress(html ,16+zlib.MAX_WBITS)	
	r_html = decompressed_data.decode('utf8')
	url_patn = re.compile(r'"url":"(.*?)","backup_url"')
	down_url = re.findall(url_patn, r_html)
	if len(down_url) == 0:
		print "正则表达式匹配失败，下载失败！"
	else:
		save_Movie(down_url[0], play_url, title)

def save_Movie(down_url, play_url, filename):
	"""
		作用：打开视频的下载地址，将视频保存到本地
		@down_url：视频的下载地址
		@filename：视频的保存名称
	"""
	headers = {
		"Host" : "upos-hz-mirrorkodo.acgvideo.com",
		"Connection" : "keep-alive",
		"Origin" : "https://www.bilibili.com",
		"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
		"Accept" : "*/*",
		"Referer" : play_url,
		"Accept-Encoding" : "gzip, deflate, br",
		"Accept-Language" : "zh-CN,zh;q=0.9"
	}
	request = urllib2.Request(down_url, headers = headers)
	video = handling_Exceptions(request)
	if video == None or video == 0:
		print "下载失败！！！"
	else:
		fullname = filename + ".mp4"
		with open(fullname, "w") as f:
			print fullname + "开始下载"
			f.write(video)
			print fullname + "下载结束"
			print "------End------"
		 

def spider(serch_url, keyword, begin_page, end_page):
	"""
		作用：哔哩哔哩网站爬虫调度器
	"""
	j = 0
	for page in range(begin_page, end_page + 1):
		tag, author, description, title, play_url = serch_Key(serch_url, keyword, page)
		for i in range (len(play_url)):
			# 调试代码
			# if i == 7:
			# 	filename = "藏族舞蹈" + str(j)
			# 	j = j + 1
			# 	info = "tag : " + tag[i] + "\r\n" + "author : " + author[i] + "\r\n" + "description : " + description[i] + "\r\n" + "title : " + title[i]
			# 	info = info.encode(encoding="utf-8")
			# 	open_Movie(play_url[i], filename)
			# 	with open(filename + ".txt", "w") as f:
			# 		f.write(info)

			filename = keyword + str(j)
			j = j + 1
			info = "tag : " + tag[i] + "\r\n" + "author : " + author[i] + "\r\n" + "description : " + description[i] + "\r\n" + "title : " + title[i]
			info = info.encode(encoding="utf-8")
			open_Movie(play_url[i], filename)
			with open(filename + ".txt", "w") as f:
				f.write(info)

def handling_Exceptions(request):
	try:
		video = urllib2.urlopen(request).read()
	except (urllib2.HTTPError, socket.error, urllib2.URLError):
		if urllib2.HTTPError:
			print "HTTPError"
			return 0
		if urllib2.URLError:
			print "URLError"
			return 0
		if socket.error:
			print "timeout"
			time.sleep(20)
			handling_Exceptions(request)
	else:	
		print "------Start------"
		return video

if __name__ == "__main__":
	"""
		作用：主函数
	"""
	keyword = raw_input("请输入要搜索视频的类型：")
	begin_page = int(raw_input("请输入起始页："))
	end_page = int(raw_input("请输入结束页："))
	serch_url = "https://api.bilibili.com/x/web-interface/search/all?"
	spider(serch_url, keyword, begin_page, end_page)




