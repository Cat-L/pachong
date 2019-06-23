# coding=UTF-8
import requests
import urllib
import os
import time
import subprocess
import random
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
# def get_ticket(song_html):
#     '''
#     作用：将url中信息解析筛选并返回结果集
#     @url:首页url
#     @key:总页数
#     '''
#     text = requests.get(song_html).text
#     globalsReExp = re.compile(r'("ticket"\s*:\s*"(?:\w|=)+")')
#     group = globalsReExp.search(text).group()
#     # print group
#     ticket = group.split()[1].strip("\"")
#     return ticket

# def searching_page(key,searchUrl):
#     #searchUrl='http://search.5sing.kugou.com/?'
#     key = key.encode('gb2312')
#     m = {'keyword': key}
#
#     search_page=open_url(searchUrl+ urllib.urlencode(m))
#     song_url=search_page.find_all("li",_class=re.compile('c\d ellipsis$'))

def getDownloadUrl(keys):
    net_key=urllib.quote(keys)
    param = {'keytext': net_key}
    searchingurl='https://www.huyahaha.com/index/sing5'
    # r=handling_Exceptions(url=searchingurl,data=param)
    r = requests.post(url=searchingurl,data=param,verify = False)
    time.sleep(3)
    return r.json()["data"]["songurl"]

def searching_page(key):
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
        # "Connection": "keep-alive",
        "Content-Length": "65",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "http://music.bbbbbb.me",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent":  random.choice(user_agent_list),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Referer": "http://music.bbbbbb.me/?name=%E4%BF%A1%E5%A4%A9%E6%B8%B8&type=5singyc",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "pgv_pvi=5584416768; pgv_si=s2776945664"
    }
    data = {
        "input": key.encode("utf-8"),
        "filter": "name",
        "type": "5singyc",
        "page": "1"
    }
    data=urllib.urlencode(data)
    search_url="http://music.bbbbbb.me/"
    search_page = handling_Exceptions(url=search_url, headers=headers, data=data)
    firstresult=search_page.json()["data"][0]
    #todo: error:IndexError: string index out of range change the data sourse
    if firstresult["url"]=="":
        print  firstresult["title"],"\n",firstresult["author"],"\n",getDownloadUrl(firstresult["link"])
        return  firstresult["title"],firstresult["author"],getDownloadUrl(firstresult["link"])
    else:
        print firstresult["title"],"\n",firstresult["author"],"\n",firstresult["url"]
        return firstresult["title"],firstresult["author"],firstresult["url"]

def handling_Exceptions(url,headers,data):
    try:
        html = requests.post(url=url,headers=headers,data=data)
        time.sleep(3)
    except (requests.exceptions.ConnectionError):
        print "requests\'exceptions"
        time.sleep(3)
        html=handling_Exceptions(url,headers,data)
        return html
    else:
        return html



def read_txt(path):
    '''
        作用：保存结果集为文件
    '''
    keys=[]
    with open(path, 'r') as f:
        for line in f:
           line = line.strip('\n')
           keys.append(line.decode('gb2312'))
    return keys

def download_mp3(downloadUrl,filepath):
    # filepath=(filepath+".mp3").decode("utf-8")
    # song_url = 'http://fs.5sing.kgimg.com/201901191716/d3f3527ef1ba2b0b99caa8ce631dd98d/G031/M05/1C/10/Xw0DAFXlzLmAbBJKAFIhD0N1uE4048.mp3'
    # filePath = '123.mp3'
    cmd = 'wget -c -T 10 -t 10 -b   -O %s %s' % (filepath, downloadUrl)
    try:
        shellcode= subprocess.Popen(args=cmd.encode("gb2312"), shell=True)
        print shellcode.pid
    # c = "wget \"%s\" -c -T 10 -t 10 --restrict-file-names=nocontrol -b -O   \"%s\"" % (downloadUrl,filepath)
    # os.system(c.encode('utf-8'))
    except ( UnicodeEncodeError):
        subprocess.call(cmd.encode("utf-8"), shell=True)
    if os.path.getsize(filepath)!=0:
        # todo:for those files size=0,chage the data sourse
        # os.rename("temp.mp3", filepath)
        print "%s download Successful \n" % (filepath)
        return True
    else:
        print "%s download Fail \n" % (filepath)
        return False

if __name__=="__main__":
    keys_path="keys.txt"
    keys=read_txt(keys_path)
    songinfos=[]
    for key in keys:
        try:
            songinfo=searching_page(key)
            songinfos.append(songinfo)
            download_mp3(songinfo[2],"%s.mp3"%key)
        except (IndexError,WindowsError):
            continue
    time.sleep(10)
