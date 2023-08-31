# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/22 12:43
@Auth ： 任维
@File ：practice.py
@IDE ：PyCharm
"""
# 冒泡排序法
lst = [2, 1, 1, 2, 3, 3, 4, 6, 2, 1, 7, 2, 8]
for i in range(len(lst)-1):


    for j in range(len(lst)-1-i):
        if lst[j] > lst[j+1]:
            lst[j], lst[j+1] = lst[j+1], lst[j]
print(lst)




