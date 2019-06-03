#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: kessil
@license: LGPL
@contact: https://github.com/kessil?tab=repositories
@software: None
@file: app.py
@time: DATA TIME
@desc: NO_DESC
'''
import os
import shutil
from datetime import datetime
import pandas as pd
from prepare_csv import prepare

# ALARM_TYPES = ["AIS报警", "E3报警", "E3误码次数超出安全范围", "E5报警", "E5误码次数超出安全范围", "LOS报警", "脱离监视状态", "ERR报警"]
# STATIONS = "武夷山北|武夷山东|建瓯西|红星线路所|南平北|古田北|闽清北|福鼎|太姥山|霞浦|福安|宁德|罗源|透堡|连江|温福线路所|福厦线路所|樟林|福州|福州南|福清|渔溪|涵江|莆田|仙游|惠安|泉州|晋江|翔安|厦门|高崎|杏林|角美|前场|漳州|漳浦|云霄|诏安|龙岩|东南线路所|马坑|龙山|南靖|草坂|矮陂线路所|古田会址|冠豸山|长汀南|龙岩动车存车场|建宁县北|泰宁|将乐|夏茂|三明|尤溪|中仙|长庆|永泰|涵江北|杜坞|上杭古田|延平|永安|双洋|漳平西|雁石南|湖一|后岭|南石"
def sulotion(base_dir):
    sources_dir = os.path.join(base_dir, "sources")
    results_dir = os.path.join(base_dir, "results")
    columns_header = ("alarm_time", "alarm_device", "alarm_router", "alarm_type")
    ALARM_TYPES = ["AIS报警", "E3报警", "E3误码次数超出安全范围", "E5报警", "E5误码次数超出安全范围", "LOS报警", "脱离监视状态", "ERR报警"]
    if os.path.exists(os.path.join(base_dir, "criteria.csv")):
        criteria = pd.read_csv(os.path.join(base_dir, "criteria.csv"), encoding="utf-8", header=None)
        STATIONS = "|".join(criteria[0])
    else:
        STATIONS = "武夷山北|武夷山东|建瓯西|红星线路所|南平北|古田北|闽清北|福鼎|太姥山|霞浦|福安|宁德|罗源|透堡|连江|温福线路所|福厦线路所|樟林|福州|福州南|福清|渔溪|涵江|莆田|仙游|惠安|泉州|晋江|翔安|厦门|高崎|杏林|角美|前场|漳州|漳浦|云霄|诏安|龙岩|东南线路所|马坑|龙山|南靖|草坂|矮陂线路所|古田会址|冠豸山|长汀南|龙岩动车存车场|建宁县北|泰宁|将乐|夏茂|三明|尤溪|中仙|长庆|永泰|涵江北|杜坞|上杭古田|延平|永安|双洋|漳平西|雁石南|湖一|后岭|南石"
    # print(STATIONS)
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    writer = pd.ExcelWriter(os.path.join(results_dir, 'pivot.xls'))
    names = [x for x in os.listdir(sources_dir) if x.endswith(".csv")]
    dfs = pd.DataFrame(columns=columns_header)
    for name in names:
        # print(name)
        df = pd.read_csv(os.path.join(sources_dir, name), sep="\t", header=0, encoding='utf-8')
        if len(df.columns) > 4:
            '''只取前4列数据，多余舍去'''
            df = df[df.columns[range(4)]]
            '''重新定义列标题'''
            df.columns = columns_header            
        dfs = pd.concat([dfs, df], ignore_index=True)

    # 当月所有报警写入csv文件
    print("所有报警[alarm_all.csv] ",dfs.shape)
    dfs.to_csv(os.path.join(results_dir, "alarm_all.csv"), sep="\t",encoding='utf-8', index=False)

    # 筛选报警,关注福州电务段管内设备
    dfs = dfs[dfs.alarm_device.str.contains(STATIONS)]
    print("福电管内[alarm_charge.csv] ",dfs.shape)
    dfs.to_csv(os.path.join(results_dir, "alarm_charge.csv"), sep="\t",encoding='utf-8', index=False)

    # 筛选报警,恢复正常不统计
    dfs = dfs[dfs.alarm_type.isin(ALARM_TYPES)]
    # 处理空值，脱离监视报警在alarm_router列为空，此时用alarm_device的值填充
    dfs.loc[dfs['alarm_router'].isnull(),'alarm_router'] = dfs[dfs['alarm_router'].isnull()].alarm_device
    dfs = dfs.reset_index(drop=True)
    print("常规报警[alarm_normal.csv] ",dfs.shape)
    dfs.to_csv(os.path.join(results_dir, "alarm_normal.csv"), sep="\t",encoding='utf-8', index=False)

    # 处理报警时间,仅关心date, hour值用来今后扩展报警时段备用
    # 利用map和lambda表达式将月和日不足两位数的前面补0,避免排序紊乱
    dfs.alarm_time = dfs.alarm_time.map(lambda x: (datetime.strptime(x, '%Y-%m-%d %H:%M:%S')).strftime('%Y-%m-%d %H:%M:%S'))
    s = dfs.alarm_time.str.split(" ", expand=True)
    s.columns = ("alarm_date", "alarm_HMS")
    dfs = dfs.join(s)
    dfs = dfs.drop(["alarm_time"], axis=1)
    dfs = dfs.reindex(columns = ("alarm_date", "alarm_HMS", "alarm_device", "alarm_router", "alarm_type"))
    ymd = dfs.alarm_date.str.split("-", expand=True)
    ymd.columns = ("alarm_year", "alarm_month", "alarm_day")
    dfs = dfs.join(ymd)
    hms = dfs.alarm_HMS.str.split(":", expand=True)
    hms.columns = ("alarm_hour", "alarm_minute", "alarm_seconds")
    dfs = dfs.join(hms)
    # print(dfs)
    # 开始进行数据透视操作
    pivot = pd.pivot_table(dfs[["alarm_month", "alarm_day", "alarm_router", "alarm_type", "alarm_device"]], index=["alarm_month", "alarm_day", "alarm_router", "alarm_type"], aggfunc='count')
    # print(pivot.shape)
    pivot.to_csv(os.path.join(results_dir, 'pivot.csv'),sep="\t", encoding='utf-8')
    pivot.to_excel(excel_writer=writer, sheet_name="Pivot_Table")

    # 分类汇总参考-TYPE
    pot_type = pd.pivot_table(dfs[["alarm_type", "alarm_device"]], index=["alarm_type"], aggfunc="count", margins=True, margins_name="总计")
    print(pot_type)
    pot_type.to_excel(excel_writer=writer, sheet_name="告警信息汇总")

    # 分类汇总参考-ROUTER
    pot_router = pd.pivot_table(dfs[["alarm_router", "alarm_device"]], index=["alarm_router"], aggfunc="count", margins=True, margins_name="总计")
    # print(pot_router)
    # pot_router = pot_router.sort("alarm_device", ascending=1)
    # print(type(pot_router))
    pot_router.to_excel(excel_writer=writer, sheet_name="线路汇总")

    # 分类汇总参考-DATE
    pot_date = pd.pivot_table(dfs[["alarm_date", "alarm_device"]], index=["alarm_date"], aggfunc="count", margins=True, margins_name="总计")
    pot_date.to_excel(excel_writer=writer, sheet_name="日期汇总")


    # 保存并关闭excel_writer
    writer.save()
    writer.close()
    print("分析结束，去results看看吧")

if __name__ == "__main__":
    print("来啦老弟！又要写通道质量监督报警分析报告啊！")
    print("Emmmm!那就再帮你一回吧！记住，我的根目录不能包含中文哟！\n")
    base_dir = os.getcwd()

    if os.path.exists(os.path.join(base_dir, "sources")):
        shutil.rmtree(os.path.join(base_dir, "sources"))
    if os.path.exists(os.path.join(base_dir, "results")):
        shutil.rmtree(os.path.join(base_dir, "results"))
    names = [x for x in os.listdir(base_dir) if os.path.isdir(x) and x not in ("venv", "venv32", "venv_x86", "__pycache__", "dist", "build")]
    if len(names) == 0:
        print("老弟的告警日志还没准备好呢！待会儿再来吧！")
    elif len(names) == 1:
        prepare(os.path.join(base_dir, names[0]))
        sulotion(base_dir)
    else:
        print("您可能需要分析的文件夹有以下几个：")
        for key, value in enumerate(names):
            print("\t%d-%s"%(key, value))
        sel = input("请选择: ")
        try:
            prepare(os.path.join(base_dir, names[int(sel)]))
        except:
            print("Input Error!")
        else:
            sulotion(base_dir)
    input("Press Enter to Exit!")