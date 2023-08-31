# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/15 11:42
@Auth ： 任维
@File ：peisong_allowance.py
@IDE ：PyCharm
"""
import requests
from master.tool.txt_rwd import dataRW
from master.data.base_data import rw_url


def peisongAllow(time):
    r_data = dataRW(rw_url, 'r')
    order_lis = []
    for i in r_data:
        order_sn = i.strip('\n')
        data = {
          'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxNTAyMTQ0IiwiY2hhbm5lbElkIjoxMDMyLCJwYUlkIjowfQ.w4xrmOEzOKBkCxovRy2_ljc-PKafVB_c5mteGFc4Qyc',
          'cityCode': '340200',
          'businessType': '1',
          'page': '1',
          'pageSize': '10',
          'startTime': time,
          'endTime': time,
          'storeName': '',
          'storeId': '',
          'merchantOrderId': order_sn,
          'orderUserId': '',
          'salesmanUserName': '',
          'salesmanUserId': '',
          'orderUserPhone': '',
          'orderStatus': '',
          'sdStartTime': '',
          'sdEndTime': '',
          'payType': '',
          'channelId': '1032'
        }
        rep = requests.request('post', 'https://proxy.wuhunews.cn/proxy/getOrderList', data=data)
        # 提取退款完成时间
        pei_song = rep.json()["data"]["data"][0]["peiSongSettlementMoney"]
        delivery_money = rep.json()["data"]["data"][0]["deliveryMoney"]
        if pei_song > delivery_money:
            abnormal_order = order_sn + "\n"
            order_lis.insert(0, abnormal_order)
    dataRW(rw_url, 'w', w_data_list=order_lis)

if __name__ == '__main__':
    time = '2023-08-13'
    peisongAllow(time)
