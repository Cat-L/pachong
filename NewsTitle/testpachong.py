# coding=UTF-8
import requests
import chardet
from bs4 import BeautifulSoup
import re


#api:



def get_text(url,key):
    result_table=[]
    count = 0
    i=1
    while(i<=key):
        last_url=url+str(i)+'.htm'
        r=requests.get(last_url)
        soup=BeautifulSoup(r.content,"lxml",from_encoding='utf-8')
        result=soup.find_all("li",id=re.compile('line_u5_\d{2}'))

        for result_string in reversed (result):
            count = count + 1
            result_table.append(str(count)+". "+result_string.string)
        #26-30行判断用于解决网页第0页内容为日期最新标题的问题
        if (i==0):
            break
        i = i + 1
        if (i == key):
            i=0




    return result_table
#  find_all("div",id='content').find_all("div",id="announce_con").find_all("div",id="con_newslist").find_all("ul").find_all("li")
# body->div(id=content,class=main) ->div(id=announce_con) ->
# div(id=con_newslist)->ul->li(id=line_u5_*)



def save_txt(path,text):
    with open(path, 'w') as f:
        for i in text:
            print i
            f.write(i.encode("utf-8")+'\n')


def spider(url,key,path):
    get_text(url,key)
    save_txt(path,get_text(url,key))

if __name__=="__main__":
    url = 'http://www.snnu.edu.cn/tzgg/'
    key = 203
    path="newstitle.txt"
    spider(url,key,path)

