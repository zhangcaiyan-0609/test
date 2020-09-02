from common.handle_config import conf
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common.handle_db import db
from common.handle_log import log
import os
from common import myddt
import unittest
import requests
from jsonpath import jsonpath
from common.handle_data import replace_data
@myddt.ddt
class TestRecharge(unittest.TestCase):
    excel = Excel(os.path.join(DATA_DIR,"cases.xlsx"), "recharge")
    cases = excel.read_data()
    @classmethod
    def setUpClass(cls):
        # 登录 获取token id
        # 登录url
        login_url = conf.get("env","base_url") + "/member/login"
        # 请求头
        headers = eval(conf.get("env","headers"))
        # 登录的参数
        mobile_phone = conf.get("test_data","mobile")
        pwd = conf.get("test_data","pwd")
        params = {
            "mobile_phone":mobile_phone,
            "pwd":pwd
        }
        # 发送登录请求
        response = requests.post(url=login_url,json=params,headers=headers)
        res = response.json()
        # 获取token
        token = jsonpath(res,"$..token")[0]
        cls.token = "Bearer" + " " + token
        cls.member_id = jsonpath(res,"$..id")[0]
    @myddt.data(*cases)
    def test_recharge(self, item):
        case_id = item["case_id"]
        # 第一步：准备数据
        url = conf.get("env", "base_url") + item["url"]
        # 请求参数
        item["data"] = replace_data(item["data"],TestRecharge)
        params = eval(item["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 请求头中要添加token
        headers["Authorization"] = self.token
        # 请求方法
        method = item["method"]
        # 预期结果
        expected = eval(item["expected"])

        sql = item["check_sql"]
        if sql:
            s_amount = db.find_data(sql.format(self.member_id))
            s_money = s_amount[0]["leave_amount"]
        # 第二步：请求接口，获取结果
        response = requests.request(url=url, method=method, json=params, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)


        # 第三步：断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            if sql:
                e_amount = db.find_data(sql.format(self.member_id))
                e_money = e_amount[0]["leave_amount"]
                self.assertEqual(float(e_money - s_money), params["amount"])

        except AssertionError as e:
            log.error("用例{}，执行未通过".format(item["title"]))
            self.excel.write_data(row=case_id +1,column=8,value="失败")
            log.exception(e)
            raise e
        else:
            log.info("用例{}，执行通过".format(item["title"]))
            self.excel.write_data(row=case_id + 1, column=8, value="通过")













        




