# coding=UTF-8
import requests.adapters
import requests
import urllib
import time
import subprocess
import random
import os
import json
import sys
import collections
import re

reload(sys)
sys.setdefaultencoding('utf-8')
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES=15

def getDownloadUrl(keys):
    net_key=urllib.quote(keys)
    param = {'keytext': net_key}
    searchingurl='https://www.huyahaha.com/index/sing5'
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
    headers = {
        "Host":"www.huyahaha.com",
        "Connection": "False",
        # "Content-Length": "46",
       "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://www.huyahaha.com",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent":  random.choice(user_agent_list),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Referer": "http://music.bbbbbb.me/?name=%E4%BF%A1%E5%A4%A9%E6%B8%B8&type=5singyc",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN",
        # "Cookie": "pgv_pvi=5584416768; pgv_si=s2776945664"
    }
    r = requests.post(url=searchingurl,data=param,verify = False)
    sleeptime = random.randint(3,5)
    time.sleep(sleeptime)
    return r.json()["data"]["songurl"]

def get_page(key,page):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
    headers = {
        "Host":"http://music.bbbbbb.me",
        "Connection": "False",
        "Content-Length": "65",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "http://music.bbbbbb.me",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent":  random.choice(user_agent_list),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Referer": "http://music.bbbbbb.me/?name=%E4%BF%A1%E5%A4%A9%E6%B8%B8&type=5singyc",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        # "Cookie": "pgv_pvi=5584416768; pgv_si=s2776945664"
    }
    data = {
        "input": key.encode("utf-8"),
        "filter": "name",
        "type": "5singyc",
        "page": page
    }
    data=urllib.urlencode(data)
    search_url="http://music.bbbbbb.me/"
    search_page = handling_Exceptions(url=search_url, headers=headers, data=data)
    #result is a json include  code,data for all the song information
    #and error
    return search_page.json()


def handling_Exceptions(url,headers,data):
    # try:
        html = requests.post(url=url,headers=headers,data=data)
        sleeptime = random.randint(5, 15)
        time.sleep(sleeptime)
    # except (requests.exceptions.ConnectionError):
    #     print "requests\'exceptions"
    #     html=handling_Exceptions(url,headers,data)
    #     sleeptime = random.randint(5, 15)
    #     time.sleep(sleeptime)
    #     return html
    # else:
        return html

def loadFont(target,name):
    songdata=collections.OrderedDict()
    songdata["作者"]='%s'%str(target['author'].encode("utf-8")).replace("\n","") ,
    songdata["年代"]=''
    songdata["器乐类型"]=''
    songdata["地域"]=''
    songdata["资源路径"]='%s'%str(target['url']).replace("\n",""),
    songdata["名称"]='%s'%str(target['title'].encode("utf-8")).replace("\n","") ,
    songdata["旋律"]=''
    songdata["URL"]='%s'%str(target['link']).replace("\n","") ,
    songdata["和声"]=''
    songdata["曲式"]=''
    songdata["民族"]=''
    songdata["声乐类型"]=''
    songdata["版权"] =''
    songdata["调式"]=''
    songdata["复调"] =''
    songdata["节奏"] =''
    songdata["关键描述"]=''
    song_json=json.dumps( songdata,ensure_ascii=False,indent=2 )
    song_json=song_json.replace("\"","").replace("[","").replace("]","")
    re.sub(r'\n\s\s,\s',',\n',song_json)
    re.sub(r'\s\n\s\s\s\s',"",song_json)
    with open("%s.json"%name,"w") as f:
        # 设置不转换成ascii  json字符串首缩进
        f.write(song_json)



def read_txt(path):
    keys=[]
    with open(path, 'r') as f:
        for line in f:
           line = line.strip('\n')
           keys.append(line.decode('gb2312'))
    return keys

def check_log(path):
    try:
        with open(path, 'r') as f:
            if f.read().find("saved")==-1:
                print f.read()
                return False
            else:
                return True
    except IOError:
        return False

def download_mp3(downloadUrl,filepath):
    cmd = 'wget -c -T 10 -t 10  -b  -O %s %s' % (filepath, downloadUrl)
    try:
        shellcode= subprocess.Popen(args=cmd.encode("gb2312"), shell=True,stdout=subprocess.PIPE)
        time.sleep(2)
    except ( UnicodeEncodeError):
        shellcode=subprocess.Popen(args=cmd.encode("utf-8"), shell=True,stdout=subprocess.PIPE)
    log_path = str(shellcode.communicate()).split("\'")[1]
    if check_log(log_path) == True:
        print "%s download Successful \n" % (filepath)
        return True
    else:
        print "%s download Fail\n" % (filepath)
        return False

def download_page(pageinfo,path):
    songinfos=pageinfo["data"]
    for song in songinfos:
        try:
            downloadurl = getDownloadUrl(song["link"])
            print  "title:", song["title"], "\n", "author:", song["author"], "\n", "link:", str(downloadurl)
            song["url"] = downloadurl
            download_mp3(downloadurl, "%s\\%s.mp3" %(path.decode("gb2312"),song["title"].replace(" ","_")))
            loadFont(song,"%s\\%s"%(path.decode("gb2312"),song["title"].replace(" ","_")))
        except IOError:
            print IOError
            continue

def search_page(key,path,page=1):
    if page==1:
        pageinfo = get_page(key,page)
    while pageinfo["error"]=="" or page<=20:
        page=page+1
        try:
            download_page(pageinfo,path=path)
            pageinfo = get_page(key, page)
        except requests.ConnectionError:
            continue


if __name__=="__main__":
    keys_path="keys.txt"
    keys=read_txt(keys_path)
    songinfos=[]
    for key in keys:
        try:
            os.mkdir(key.encode("gb2312"))
            search_page(key,page=1,path=key.encode("gb2312"))
        except (IndexError,WindowsError):
            continue
    time.sleep(10)