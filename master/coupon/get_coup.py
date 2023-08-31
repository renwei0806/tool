# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/17 16:54
@Auth ： 任维
@File ：get_coup.py
@IDE ：PyCharm
"""
import requests
from master.tool.txt_rwd import dataRW
from master.data.base_data import rw_url


def getcoupon():
    # 以列表的形式读取文本中的数据
    cid = dataRW(rw_url, 'r')
    # 分离出手机号
    phone_num = cid[0].strip('\n')
    del cid[0]
    # 分离出用户ID
    u_id = cid[0].strip('\n')
    del cid[0]
    # 分离出券包ID
    activity_id = cid[0].strip('\n')
    del cid[0]
    # 创建空列表，存放已经抢到的消费券
    coup = []
    # 根据用户ID生成用户token
    u_url = "http://waimai.wuhunews.cn/Test/createToken"
    u_data = {
        "userId": u_id,
        "channelId": '1032'
    }
    u_info = requests.request('post', u_url, data=u_data)
    u_token = u_info.json()['data']
    # 根据活动券ID进行循环
    for i in cid:
        c_id = i.strip('\n')
        # 发起抢券，根据返回的提示判断券是否抢到，结束一张券进入下一张抢券。
        while True:
            # 抢券参数
            c_data = {
                'couponId': c_id,
                'activityId': activity_id,
                'sourceChannel': 'djms',
                'phoneNum': phone_num,
                'lon': '',
                'lat': '',
                'channelId': '1032',
                'token': u_token
            }
            # 抢券URL
            c_url = "https://coupon.wuhunews.cn/SmallShopMerchant/FrontEnd/Home/receiveConsumerCoupon"
            # 抢券请求
            rep = requests.request('post', c_url, data=c_data)
            # 根据抢券返回信息判断是否继续抢券，如果已经无法继续抢得改券进入下一张抢券
            msg = rep.json()['msg']
            if '恭喜您' in msg or '已经' in msg:
                coup.insert(0, c_id)
                break
            elif '上限' in msg or '抢完' in msg or '结束' in msg or '未开始' in msg:
                break
    if len(coup) == 0:
        print('您没有抢到券')
    else:
        print(f'您已经抢到了了{len(coup)}张券，券ID分别是：{coup}')


if __name__ == '__main__':
    getcoupon()
