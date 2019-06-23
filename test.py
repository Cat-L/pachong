# coding=UTF-8
import requests
import chardet
from bs4 import BeautifulSoup
import re
import urllib.parse
import urllib.request

import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# def find_depth(res):
#     soup = BeautifulSoup(res.text,"html.parser")
#     depth = soup.find('span',class_='next').previous_sibling.previous_sibling.text
#     return int(depth)
#
# def save_txt(path,text):
#     with open(path, 'w') as f:
#         f.write(text)


if __name__ == '__main__':


    fanyi = input('输入你想要翻译的句子')
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {}
    data['i'] = '我爱你'
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = '15510064582010'
    data['sign'] = 'adaa64145192d9367024933a9a16955b'
    data['ts'] = '1551006458201'
    data['bv'] = 'bbb3ed55971873051bc2ff740579bb49'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_REALTIME'
    data['typoResult'] = 'false'
    data = bytes(urllib.parse.urlencode(data).encode('utf-8'))
    res = urllib.request.Request(url, data)
    response = urllib.request.urlopen(res)
    html = response.read().decode('utf-8')
    print(html['translateResult'][0][0]['tgt'])
