#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: kessil
@license: LGPL
@contact: https://github.com/kessil?tab=repositories
@software: None
@file: prepare_csv.py
@time: DATA TIME
@desc: NO_DESC
'''
import os
import re
import codecs

def prepare(child_dir:str):
    '''文件名中月份和日期只有一位数时给文件排序带来挑战，该函数将前加0'''
    parent_dir = os.path.dirname(child_dir)
    sources_dir = os.path.join(parent_dir, "sources")
    if not os.path.exists(sources_dir):
        os.mkdir(sources_dir)
    names = [x for x in os.listdir(child_dir) if x.endswith(".xls") or x.endswith(".xlsx")]
    if len(names) > 0:
        for name in names:
            x = re.match(r'告警信息_(\d*)年(\d*)月(\d*)日', name)
            new_name = 'Alarm_%4d_%02d_%02d.csv'%(int(x.group(1)), int(x.group(2)), int(x.group(3)))
            # os.rename(os.path.join(path, name), os.path.join(path, new_name))
            
            # 保存为utf-8格式
            origin_file = codecs.open(os.path.join(child_dir, name), 'r', 'ansi')
            data = origin_file.read()
            new_file = codecs.open(os.path.join(sources_dir, new_name), 'w', 'utf-8')
            new_file.write(data)

        return True
    else:
        return False


if __name__ == "__main__":
    path = "C:/Users/vince/Documents/2018通道质量监督分析报告/7月份通道质量监督报警分析报告/通道质量监督报警18年07月"
    print(prepare(path))

