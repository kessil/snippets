#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: kessil
@license: LGPL
@contact: https://github.com/kessil?tab=repositories
@software: None
@file: category.py
@time: DATA TIME
@desc: NO_DESC
'''
from time import sleep
from pathlib import Path
from fake_useragent import UserAgent
from lxml import etree
import requests
from mzitu import Mzitu

class Category(object):
    '''下载一个分类'''
    def __init__(self, url, path='./images'):
        self.url = url
        self.path = path
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0" # UserAgent().random
        self.headers = {
            "Host": "www.mzitu.com",
            "User-Agent": self.user_agent
        }
        r = requests.get(self.url, headers=self.headers)
        if r.status_code != 200:
            return False
        # print(r.text)
        html = etree.HTML(r.text)
        self.total_page = int(html.xpath('//nav[@class="navigation pagination"]/div[@class="nav-links"]/a[last()-1]/text()')[0])
    
    def __repr__(self):
        return f'URL: {self.url}\nTotalPage: {self.total_page}'

    def start(self):
        for i in range(1, self.total_page+1):
            url = "%s/page/%d"%(self.url, i)
            print("Loading %s..."%url)
            r = requests.get(url, headers=self.headers)
            if r.status_code != 200:
                return False
            html = etree.HTML(r.text)
            pins = html.xpath('//div[@class="postlist"]/ul[@id="pins"]/li/a/@href')
            for pin in pins:
                print("Accessing URL: %s..."%pin)
                sleep(2)
                m = Mzitu(pin, self.path)
                m.start()

        return True
                






if __name__ == "__main__":
    c = Category(url="https://www.mzitu.com/mm/")
    print(c)
    c.start()