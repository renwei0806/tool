# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/15 15:00
@Auth ： 任维
@File ：txt_rwd.py
@IDE ：PyCharm
"""
def dataRW(rw_url, rw_mode, w_data_list=[]):
    if rw_mode == 'r':
        with open(rw_url, 'r', encoding='utf-8') as rd:
            r_data = rd.readlines()
            rd.close()
            return r_data
    if rw_mode == 'w':
        with open(rw_url, 'w', encoding='utf-8')as wd:
            wd.writelines(w_data_list)
            wd.close()
