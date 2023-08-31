# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/30 15:52
@Auth ： 任维
@File ：coupon_data.py
@IDE ：PyCharm
"""
import requests
from read_write_yaml import ReadWriteYaml


class CouponsStatistics:
    def __init__(self):
        # 统计参数值初始化
        self.page = 1  # 页面检索初始值
        self.coupons_id = []  # 发券券包ID存储
        self.max_num_sum = 0  # 发券张数总和
        self.coupon_count = 0  # 发券次数统计
        self.money_sum = 0  # 发券金额和
        self.order_total_money = 0  # 订单总金额
        self.order_total_discount_money = 0  # 订单总优惠
        self.receive_total_rows = 0  # 消费券领取数量
        self.order_total_rows = 0  # 消费订单总数
        self.path = "../data/coupon_params.yaml"
        self.statistical_result = {}

    def data_statistics(self):
        """对发放金额大于1万的券包进行统计，并统计出：发券张数总和、发券次数、发券金额和、券包ID"""
        for status in range(1, 3):
            while True:
                # 定义消费券url和参数
                url = "https://op.wuhunews.cn/ActivityCoupon/Backstage/couponPackageList"
                # 从yaml数据文件中获取请求中的data数据
                params = ReadWriteYaml(self.path)
                coupons_params = params.read_all_yaml()
                coupons_param = coupons_params[0]
                # 插入：页面变量、是否过期状态。
                coupons_param["status"] = status
                coupons_param["page"] = self.page
                resp = requests.request('post', url, data=coupons_param)
                jsons = resp.json()
                coupons = jsons["data"]["data"]
                """判断出符合条件的券包，并统计出：发券张数总和、发券次数、发券金额和、券包ID"""
                if coupons:
                    self.page += 1  # 从第一页开始查起，统计完一页更换另一页
                    for coupon in coupons:
                        # 仅对券包发券金额大于一万的券包进行统计
                        if coupon["money"] >= 10000:
                            self.max_num_sum += coupon["maxNum"]
                            self.coupon_count += 1
                            self.money_sum += coupon["money"]
                            self.coupons_id.append(coupon["id"])
                else:
                    break
        for acStatus in range(1, 3):
            for pcId in self.coupons_id:
                """准备请求参数，接口请求参数：data，从yaml中获取；插入：券包ID变量、券的使用核销区分变量"""
                params = ReadWriteYaml(self.path)
                coupons_param = params.read_all_yaml()[1]
                url = "https://coupon.wuhunews.cn/SmallShopMerchant/Backstage/OrderManageNew/consumptionVolumeOrder"
                coupons_param["pcId"] = pcId
                coupons_param["acStatus"] = acStatus
                """对已领取的券：领取数量统计；对已核销的券：已领取券、已核销数量、消费总金额、优惠总金额进行统计"""
                if acStatus == 2:
                    resp = requests.request('post', url, data=coupons_param)
                    jsons = resp.json()["data"]
                    self.order_total_money += float(jsons["totalMoney"])
                    self.order_total_discount_money += float(jsons["totalDiscountMoney"])
                    self.order_total_rows += jsons["totalRows"]
                    self.receive_total_rows += jsons["totalRows"]
                else:
                    coupons_param["acStatus"] = acStatus
                    resp = requests.request('post', url, data=coupons_param)
                    jsons = resp.json()["data"]
                    self.receive_total_rows += jsons["totalRows"]
        """将统计结果放入字典中存储起来，并返回字典"""
        self.statistical_result["make_coupon_sum"] = self.max_num_sum  # 发券数量总和
        self.statistical_result["receive_coupon_sum"] = self.receive_total_rows  # 领券数量总和
        self.statistical_result["use_coupon_sum"] = self.order_total_rows  # 券核销数量总和
        self.statistical_result["make_coupon_money_sum"] = self.money_sum  # 消费券发放金额总和
        self.statistical_result["user_pay_money"] = self.order_total_money - self.order_total_discount_money  # 用户实付金额
        self.statistical_result["use_coupon_order_money_sum"] = self.order_total_money  # 消费券核销总金额
        self.statistical_result["use_coupon_money_sum"] = self.order_total_discount_money  # 消费券核销优惠金额
        self.statistical_result["coupon_usage_rate"] = self.order_total_discount_money / self.money_sum  # 消费券的核销率
        self.statistical_result["coupon_promote_consume_ratio"] = self.order_total_discount_money / self.money_sum  # 消费券的带动比
        self.statistical_result["activity_count"] = self.coupon_count  # 消费券的活动次数
        return self.statistical_result


# if __name__ == '__main__':
#     statistical_result = CouponsStatistics().data_statistics()
#     print(statistical_result)
