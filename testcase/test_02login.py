from common import myddt
import unittest
from common.handle_config import Config
from common.handle_excel import Excel
from common.handle_log import log
from common.handle_path import DATA_DIR
import os
from common.handle_config import conf
import requests
from jsonpath import jsonpath
import random
@myddt.ddt
class TestLogin(unittest.TestCase):
    excel = Excel(os.path.join(DATA_DIR,'cases.xlsx'), 'login')
    case = excel.read_data()

    @myddt.data(*case)
    def test_login(self,case_data):
        # 准备用例数据
        # 请求接口
        url = conf.get("env","base_url") + case_data["url"]
        # 请求头
        headers = eval(conf.get("env","headers"))

        case_row = case_data["case_id"] + 1
        # 预期结果
        excepted = eval(case_data["expected"])
        # 请求参数
        if "*phone*" in case_data["data"]:
            phone = self.random_phone()
            case_data["data"] = case_data["data"].replace("*phone*",phone)

        params = eval(case_data["data"])
        # 请求方法
        method = case_data["method"]

        # 调用接口，获取实际结果
        response = requests.request(url=url,method=method,json=params,headers=headers)
        res = response.json()
        # 断言
        try:
            self.assertEqual(excepted["code"],res["code"])
            self.assertEqual(excepted["msg"],res["msg"])
        except AssertionError as e:
            self.excel.write_data(row=case_row, column=8, value='失败')
            log.error("{}用例执行失败，失败信息如下：".format(case_data['title']))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=case_row, column=8, value='通过')
            log.info("{}用例执行通过".format(case_data['title']))

    @staticmethod
    def random_phone():
        phone = "176"
        for i in range(8):
            i = random.randint(0,9)
            phone += str(i)
        return phone




