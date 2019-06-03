#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: kessil
@license: LGPL
@contact: https://github.com/kessil?tab=repositories
@software: None
@file: app.py
@time: DATA TIME
@desc: bing wallpaper hunter in 02:00pm. everyday
'''

from pathlib import Path
import requests
from lxml import etree
from datetime import datetime


def download_bing_wallpaper(home_url="https://cn.bing.com", save_path="./wallpapers"):
    '''下载bing每日壁纸'''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
        "Host": "cn.bing.com"
    }
    home_page = requests.get(home_url, headers=headers)
    if home_page.status_code != 200:
        return home_page.status_code
    html = etree.HTML(home_page.text)
    bglink = html.xpath('//head/link[@id="bgLink"]/@href')[0]
    bg_url = home_url + bglink
    image_page =  requests.get(bg_url, headers=headers)
    if image_page.status_code != 200:
        return image_page.status_code
    image_content = image_page.content
    file_dir = Path(save_path).joinpath(datetime.now().strftime("%U"))
    file_dir.mkdir(parents=True, exist_ok=True)
    file_name = file_dir.joinpath("%s.jpg"%datetime.now().strftime("%Y-%m-%d-%A"))
    with open(str(file_name), 'wb') as fp:
        fp.write(image_content)
    print("%s download success!"%bg_url)
        

if __name__ == "__main__":
    download_bing_wallpaper()
    # download_bing_wallpaper(save_path="/media/pi/raspdisk/wallpapers") 


