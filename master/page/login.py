# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/29 19:05
@Auth ： 任维
@File ：login.py
@IDE ：PyCharm
"""
import requests


url = "https://alphadj-uc.fpwan.com/userCenter/phoneLogin"
# # 取消警告
# requests.packages.urllib3.disable_warnings()
params = {
    "channelId": '1045',
    "phone": '15571610806',
    "code": '8888',
    "systemType": 'android',
    "action": 'checkCode'
}
resp = requests.request(method='get', url=url, params=params)
print(resp.json())
