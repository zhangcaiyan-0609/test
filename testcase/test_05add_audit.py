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
class TestAdd(unittest.TestCase):
    excel = Excel(os.path.join(DATA_DIR,"cases.xlsx"),"add")
    cases = excel.read_data()
    @myddt.data(*cases)
    def test_add(self,item):
        # 第一步：获取参数
        case_id = item["case_id"]
        # 请求的url
        url = conf.get("env","base_url") + item["url"]
        # 请求的方法
        method = item["method"]
        # 请求的headers
        headers = eval(conf.get("env","headers"))
        if item["interface"] == "add":
            headers["Authorization"] = self.token
        # 请求的参数
        item["data"] = replace_data(item["data"],TestAdd)
        params = eval(item["data"])
        # 预期的结果
        expected = eval(item["expected"])
        # 判断执行前的数据库状态
        sql = item["check_sql"]
        # 第二步 发送请求
        response = requests.request(url=url,method=method,json=params,headers=headers)
        res = response.json()
        if item["interface"] == "login":
            # 提取token和用户id保存为类属性
            TestAdd.token = "Bearer" + " " + jsonpath(res, "$..token")[0]
            TestAdd.member_id = jsonpath(res, "$..id")[0]

        print("预期结果：", expected)
        print("实际结果：", res)
        try:
            self.assertEqual(res["code"],expected["code"])
            self.assertEqual(res["msg"],expected["msg"])
            if item["interface"] == "add":
                if sql:
                    sql = replace_data(sql, TestAdd)
                    res = db.find_data(sql)
                self.assertTrue(res)
        except AssertionError as e:
            log.error("用例执行失败：{}".format(item["title"]))
            log.exception(e)
            raise e
            self.excel.write_data(row=case_id + 1, column=8, value="失败")
        else:
            log.info("用例执行通过：{}".format(item["title"]))
            self.excel.write_data(row=case_id + 1, column=8, value="通过")
