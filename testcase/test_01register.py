
import os
import random
import unittest
import requests
from common.handle_excel import Excel
from common.handle_log import log
from common.handle_path import DATA_DIR
from common import myddt
from common.handle_config import conf
from common.handle_db import db


@myddt.ddt
class TestRegister(unittest.TestCase):
    excel = Excel(os.path.join(DATA_DIR, "cases.xlsx"), "register")
    cases = excel.read_data()

    @myddt.data(*cases)
    def test_register(self, item):
        # 第一步：准备数据
        # /member/register
        # http://api.lemonban.com/futureloan
        url = conf.get("env", "base_url") + item["url"]
        headers = eval(conf.get("env", "headers"))
        # 判断参数中是否有手机号需要替换
        if "#phone#" in item["data"]:
            phone = self.random_phone()
            # 将参数中的#phone#替换成手机号码
            item["data"] = item["data"].replace("#phone#", phone)

        params = eval(item["data"])
        expected = eval(item["expected"])
        method = item["method"]
        # 第二步：请求接口，获取实际结果
        response = requests.request(url=url, method=method, json=params, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", response.text)
        # 第三步：断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            sql = item["check_sql"]
            print(type(sql))

            if sql:
                sql2 = sql.format(params["mobile_phone"])
                res = db.find_data(sql2)
                # 断言是否能够查询到数据
                self.assertTrue(res)
        except AssertionError as e:
            log.error("用例{}，执行未通过".format(item["title"]))
            log.exception(e)
            raise e
        else:
            log.info("用例{}，执行通过".format(item["title"]))

    @staticmethod
    def random_phone():
        """随机生成一个未注册手机号"""
        while True:
            phone = "131"
            for i in range(8):
                i = random.randint(0, 9)
                phone += str(i)
            # 判断改手机号是否已注册
            sql = "SELECT * FROM futureloan.member WHERE mobile_phone={}".format(phone)
            res = db.find_data(sql)
            if not res:
                return phone
