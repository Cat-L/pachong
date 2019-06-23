#encoding=utf-8
import requests
from bs4 import BeautifulSoup
import re

def open_url(url):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res = requests.get(url,headers=headers)
    return res
#找通告标题
def find_tg(res):
    soup=BeautifulSoup(res.text,"html.parser")
    tg=[]
    targets =soup.find_all("div",class_="con_newslist")
    for each in targets:
        tg.extend(each.a.text)
        return tg
#找出一共多少个页面
def find_depth(res):
    soup = BeautifulSoup(res.text,"html.parser")
    depth = soup.find('span',class_='next').previous_sibling.previous_sibling.text
    return int(depth)

def main():
    host = "http://www.snnu.edu.cn/tzgg.htm"
    res = open_url(host)
    depth=find_depth(res)
    result = []
    for i in range(depth):
        url = 'http://www.snnu.edu.cn/tzgg'+'depth-i'+'.htm'
        res = open_url(url)
        a=find_tg(res)
        a.extend(find_tg(res))
        for p in a:
            print p
            # with open("学校官网通告.txt","w",encoding="utf-8")as f:
            #     f.write(p)


if __name__=="__main__":
    main()