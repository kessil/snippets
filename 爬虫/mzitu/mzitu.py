#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: kessil
@license: LGPL
@contact: https://github.com/kessil?tab=repositories
@software: None
@file: mzitu.py
@time: DATA TIME
@desc: NO_DESC
'''
from datetime import datetime
import re
from pathlib import Path
import requests
from lxml import etree
from fake_useragent import UserAgent

class Mzitu(object):
    '''Mzitu类的功能定位：给一个图集URL(画板)，将整个图集所有图片下载下来'''
    def __init__(self, url, path='./images'):
        self.url = url
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0" # UserAgent().random
        print(self.user_agent)
        self.headers = {
            "Host": "www.mzitu.com",
            "User-Agent": self.user_agent
        }
        
        r = requests.get(self.url, headers=self.headers)
        if r.status_code != 200:
            return False
        html = etree.HTML(r.text)
        self.title = html.xpath('//h2[@class="main-title"]/text()')[0] or ''
        self.count = int(html.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]) or 0
        self.category = html.xpath('//div[@class="main-meta"]/span[1]/a/text()')[0] or "未分类"
        self.timestamp = re.findall(r'发布于 (.*)', html.xpath('//div[@class="main-meta"]/span[2]/text()')[0])[0] or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.visits = int(re.findall(r'\d+', html.xpath('//div[@class="main-meta"]/span[3]/text()')[0])[0]) or 0
        self.img_src = html.xpath('//div[@class="main-image"]//img/@src')[0] # 如果网站文件命名符合规律，可以采用构造图片链接法，以节省大量网络资源

        # 初始化目录
        self.path = Path(path).joinpath("%s_%s"%(self.category, re.sub(r'[\/:*?"<>|].', '', self.title))) # 剔除目录非法字符
        self.path.mkdir(parents=True, exist_ok=True)

        print(self.title)
        
        with open(str(self.path.joinpath('info.txt')), 'w') as fp:
            fp.write(f'<class Mzitu>\nTitle: {self.title}\nURL: {self.url}\nCount: {self.count}\nCategory: {self.category}\nTimeStamp: {self.timestamp}\nVisits: {self.visits}\n')

    def __repr__(self):
        return f'<class Mzitu>\nTitle: {self.title}\nURL: {self.url}\nCount: {self.count}\nCategory: {self.category}\nTimeStamp: {self.timestamp}\nVisits: {self.visits}\n'

    def start(self):
        for i in range(1,self.count+1):
            url = "%s/%d"%(self.url, i)
            # print(url)
            r = requests.get(url, self.headers)
            if r.status_code != 200:
                return False
            html = etree.HTML(r.text)
            src = html.xpath('//div[@class="main-image"]//img/@src')[0]
            print('Downloading %s...'%src)
            r2 = requests.get(src, headers={
                    "Host": "i.meizitu.net",
                    "User-Agent": self.user_agent,
                    "Referer": url
                })
            if r2.status_code != 200:
                return False

            filename = self.path.joinpath("%02d.jpg"%i)
            # print(filename)
            with open(str(filename), 'wb') as fp:
                fp.write(r2.content)


if __name__ == "__main__":
    m = Mzitu("https://www.mzitu.com/154786")
    print(m)
    m.start()

