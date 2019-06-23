# coding=UTF-8
import requests
from bs4 import BeautifulSoup
import re


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
            # "Cookie": "	JSESSIONID=B772991E3326DBAAA07F25F2F5800E66",

            "Host": "service.5sing.kugou.com",
            # 用于指定请求资源的Internet主机和端口号，必须表示请求URL的原始服务
            # 器或网关的位置

            # "If-Modified-Since" : "Tue, 21 Aug 2018 06:25:24 GMT",
            # "If-None-Match" : 'W/"5b7bb054-35ea"',
            "Proxy-Connection": "keep-alive",

            "Referer": "http://5sing.kugou.com/index.html",
            # 对付“反盗链”(服务器会识别headers中的referer是不是它自己,如果不是则不响应)
            "Upgrade-Insecure-Requests": "1",
            # 使服务器将https可以转化为http
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            # User-Agent用于辨别浏览器身份，伪装自己的爬虫身份以防止服务器拒绝爬虫访问
            "Connection": "keep-alive",
            # Accept: */*
            "Accept-Encoding": "gzip, deflate",
            "Cookie": "UM_distinctid=16859990fb232a-05bd18e09bef6-6313363-144000-16859990fb4b0; 5sing_ssid=vg5bg3f239t9hgsd2ft081ggp2; 5SING_TAG_20190117=_ST-0.STW-0.SC-0.PL-0.FX-0.ZF-0.ZC-0.XZ-4.DZ-0%7CHY_ST-0.STW-0.SC-0.PL-0.FX-0.ZF-0.ZC-0.XZ-1.DZ-0; 5sing_gid=8579ce078ef94463b5c2ce47b9550830; kg_mid=9ec2a99514fd8189ccca9142da30bfb4; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1547693234; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1547693272; 5sing_auth=85DoXi5KV0CmWGWQQgRVNbfbuH0kT8AHby5WeDkZ/rcA3Q5wonprCA==; 5sing_user_info=a%3A3%3A%7Bs%3A7%3A%22wsingId%22%3Bi%3A69725713%3Bs%3A8%3A%22username%22%3Bs%3A15%3A%22WhoamI_69725713%22%3Bs%3A6%3A%22avatar%22%3Bs%3A65%3A%22http%3A%2F%2Fwsing.bssdl.kugou.com%2F03b42d62450ffcb05428b958512bea22.jpg%22%3B%7D",
        }
    #request = requests.get(url,hearders=headers)
    request = requests.get(url)
    soup = BeautifulSoup(request.content, "lxml", from_encoding='utf-8')
    return soup


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
        result=open_url(last_url).find_all("li",id=re.compile('line_u5_\d{1,2}'))#此处使用正则表达式筛选页面信息

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
    url = 'http://5sing.kugou.com/my/#page=1'
    # key = 203
    # path="newstitle.txt"
    # spider(url,key,path)
    print open_url(url)



