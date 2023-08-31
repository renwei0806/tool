# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/29 11:25
@Auth ： 任维
@File ：read_write_yaml.py
@IDE ：PyCharm
"""
import io

import yaml


class ReadWriteYaml:
    def __init__(self, path, mode='r', write_data=None):
        self.path = open(path, mode=mode, encoding='utf-8')
        self.write_data = write_data

    # yaml数据读取
    def read_yaml(self):
        try:
            data = yaml.load(self.path, Loader=yaml.FullLoader)
            return data

        except io.UnsupportedOperation:
            return '请使用读取的方式打开文件'

    # yaml同页面多组数据读取
    def read_all_yaml(self):
        lists = []
        datas = yaml.load_all(self.path, Loader=yaml.FullLoader)
        for data in datas:
            lists.append(data)
        return lists

    # yaml数据写入（覆盖的方式）sort_keys：是否对键进行排序，默认否；
    def write_yaml(self, sort_keys=False):
        try:
            yaml.dump(self.write_data, self.path, sort_keys=sort_keys)
            return '写入成功'
        except io.UnsupportedOperation:
            return '请配置打开的方式为写入“w”'


if __name__ == '__main__':
    path = "../data/coupon_params.yaml"
    coupons = ReadWriteYaml(path)
    coupons = coupons.read_all_yaml()
    print(type(coupons))
