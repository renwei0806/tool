# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/15 10:33
@Auth ： 任维
@File ：refund_order.py
@IDE ：PyCharm
"""
import requests
from master.tool.txt_rwd import dataRW
from master.data.base_data import rw_url


def refundOrder(time):
    r_data = dataRW(rw_url, 'r')
    order_lis = []
    for i in r_data:
        order_sn = i.strip('\n')
        data = {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxNTcxODk1IiwiY2hhbm5lbElkIjoxMDMyLCJzZXNzaW9uSWQiOiJiNjVkaTdpZmNpNTQyODFkYnMyM2wzZGZyYiIsInBhSWQiOiI5MyJ9.uNuiqIE_KS_wyFqY2SkeHDnj-MTQhW57Ljm2vwRJ7W8",
            "page": 1,
            "size": 10,
            "cityCode": 340200,
            "orderType": 3,
            "startTime": '2023-08-01',
            "endTime": '2023-08-17',
            "storeId": 0,
            "storeName": 0,
            "wmoOrderSn": order_sn,
            "userId": 0,
            "chargebackStartTime": '2023-08-01',
            "chargebackEndTime": '2023-08-14',
            "channelId": 1032
        }
        rep = requests.request('post',
                               'https://waimai.wuhunews.cn/proxy/order/saleList',
                               data=data)
        # 提取退款完成时间
        lists = rep.json()["data"]["lists"]
        if lists != None:
            chargeback_time = lists[0]["chargebackTime"]
            if time not in chargeback_time:
                abnormal_order = order_sn + "\n"
                order_lis.insert(0, abnormal_order)
        else:
            print('订单不存在')
    dataRW(rw_url, 'w', w_data_list=order_lis)


if __name__ == '__main__':
    time = '2023-08-16'
    refundOrder(time)