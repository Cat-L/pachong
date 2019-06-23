# encoding=utf-8


import urllib
import urllib2
import time
import sys
from bs4 import BeautifulSoup
import socket
import ssl
import os

# 设置系统编码格式

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "_name_":
    url = 'http://www.snnu.edu.cn/tzgg/'
    save_path = ''
    key = 203


def spider(url, save_path, key):
    i = 1;
    while (i < key):
        thisUrl = url + str(i) + '.htm'

        html = openUrl(thisUrl)
        # make a function to get the url
        save_txt(html, save_path)

        i = i + 1


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


def openUrl(url):
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

    request = urllib2.Request(url, headers=headers)
    html = handling_Exceptions(request)
    return html


def handling_Exceptions(request):
    """
		作用：处理异常；
	"""
    try:
        html = urllib2.urlopen(request).read().decode('utf-8')
    # 字符编码
    except (urllib2.HTTPError, socket.error):
        if urllib2.HTTPError:
            print "HTTPError"
            return 0
        if socket.error:
            #套接字错误
            print "timeout"
            time.sleep(20)
            handling_Exceptions(request)
    else:
        return html


def save_txt(html, path):
    return
