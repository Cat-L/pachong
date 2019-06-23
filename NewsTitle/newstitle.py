# coding=UTF-8
import requests
from bs4 import BeautifulSoup
import re
import socket
import time

# def handling_Exceptions(request):
# 	"""
# 		作用：处理异常；
# 	"""
# 	try:
# 		html = requests.urlopen(request).read().decode('utf-8')
# 	except (requests.HTTPError, socket.error):
# 		if requests.HTTPError:
# 			print "HTTPError"
# 			return 0
# 		if socket.error:
# 			print "timeout"
# 			time.sleep(20)
# 			handling_Exceptions(request)
# 	else:
# 		return html

def open_url(url):
    '''
    #作用：打开url并进行页面解析
    @url：当前页URL
    @返回soup
    '''
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # 请求报头域，用于指定客户端接受哪些信息
        "Accept-Language": "zh-CN,zh;q=0.9",
        # （目测是）对页面的语言选择
        "Cache-Control": "max-age=0",
        # 用于指定缓存指令，缓存指令是单向、独立的
        "Cookie": "	JSESSIONID=B772991E3326DBAAA07F25F2F5800E66",

        "Host": "http://www.snnu.edu.cn/",
        # 用于指定请求资源的Internet主机和端口号，必须表示请求URL的原始服务
        # 器或网关的位置

        # "If-Modified-Since" : "Tue, 21 Aug 2018 06:25:24 GMT",
        # "If-None-Match" : 'W/"5b7bb054-35ea"',
        "Proxy-Connection": "keep-alive",

        "Referer": "http://www.snnu.edu.cn/tzgg/203.htm",
        # 对付“反盗链”(服务器会识别headers中的referer是不是它自己,如果不是则不响应)
        "Upgrade-Insecure-Requests": "1",
        # 使服务器将https可以转化为http
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        # User-Agent用于辨别浏览器身份，伪装自己的爬虫身份以防止服务器拒绝爬虫访问
    }
    #request = requests.get(url,hearders=headers)
    request = requests.get(url)
    html=handling_Exceptions(request)
    return html

def get_text(url,key):
    '''
    作用：将url中信息解析筛选并返回结果集
    @url:首页url
    @key:总页数
    '''
    result_table=[]#结果集
    count = 0#每行标题计数
    i=1#循环变量
    while(i<=key):
        last_url=url+str(i)+'.htm'
        html=open_url(last_url)
        result=BeautifulSoup(html.content, "lxml", from_encoding='utf-8').find_all("li",id=re.compile('line_u5_\d{0,2}'))#此处使用正则表达式筛选页面信息

        for result_string in reversed (result):
            count = count + 1
            result_table.append(str(count)+". "+result_string.string)

        #56-60行判断用于解决网页第0页内容为日期最新标题的问题
        if (i==0):
            break
        i = i + 1
        if (i == key):
            i=0
    return result_table

def save_txt(path,text):
    '''
        作用：保存结果集为文件
    '''
    with open(path, 'w') as f:
        for i in text:
            print i
            f.write(i.encode("utf-8")+'\n')

def spider(url,key,path):
    save_txt(path,get_text(url,key))

if __name__=="__main__":
    url = 'http://www.snnu.edu.cn/tzgg/'
    key = 203
    path="newstitle.txt"
    spider(url,key,path)