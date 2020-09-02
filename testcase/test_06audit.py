
from common.handle_config import conf
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common.handle_db import db
from common.handle_log import log
import os
import random
from common import myddt
import unittest
import requests
from jsonpath import jsonpath
from common.handle_data import replace_data
@myddt.ddt
class TestAudit(unittest.TestCase):
    excel_audit = Excel(os.path.join(DATA_DIR,"cases.xlsx"),"audit")
    case_audit = excel_audit.read_data()
    @classmethod
    def setUpClass(cls):
        """
        普通用户登录，管理员登录
        """
        login_url = conf.get("env", "base_url") + "/member/login"
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 登录的参数
        mobile_phone = conf.get("test_data", "mobile")
        pwd = conf.get("test_data", "pwd")
        params = {
            "mobile_phone": mobile_phone,
            "pwd": pwd
        }
        # 发送登录请求
        response = requests.post(url=login_url, json=params, headers=headers)
        res = response.json()
        # 获取token
        token = jsonpath(res, "$..token")[0]
        cls.token = "Bearer" + " " + token
        cls.member_id = jsonpath(res, "$..id")[0]

        # 管理员登录
        login_url = conf.get("env", "base_url") + "/member/login"
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 管理员登录的参数
        admin_params = {
            "mobile_phone": conf.get("test_data","admin_mobile"),
            "pwd": conf.get("test_data","admin_pwd")
        }
        # 发送登录请求
        response = requests.post(url=login_url, json=admin_params, headers=headers)
        res = response.json()
        # 获取管理员的token
        cls.admin_token = "Bearer" + " " + jsonpath(res, "$..token")[0]

    def setUp(self):
        """
        使用普通用户添加项目,然后提取项目ID
        """
        add_url = conf.get("env","base_url") + "/loan/add"
        headers = eval(conf.get("env","headers"))
        headers["Authorization"] = self.token
        params = {
            "member_id":self.member_id,
            "title":"sun".format(random.randint(0,100)),
            "amount":1000,
            "loan_rate":5.76,
            "loan_term":6,
            "loan_date_type":1,
            "bidding_days":1
        }
        response = requests.request(url=add_url,method="post",json=params,headers=headers)
        res = response.json()
        # 将项目ID保存为类属性
        TestAudit.project_id = jsonpath(res,"$..id")[0]
    @myddt.data(*case_audit)
    def test_audit(self,item):
        #第一步：请求参数
        case_id = item["case_id"]
        url = conf.get("env", "base_url") + item["url"]
        method = item["method"]
        headers = eval(conf.get("env","headers"))
        headers["Authorization"] = self.admin_token
        print(headers)
        item["data"] = replace_data(item["data"],TestAudit)
        params = eval(item["data"])
        expected = eval(item["expected"])
        # 数据库的校验
        sql = item["check_sql"]
        #第二步：发送请求
        response = requests.request(url= url,method=method,json=params,headers=headers)
        res = response.json()
        print("实际结果",res)
        print("预期结果",expected)
        #第三步： 断言
        try:
            self.assertEqual(res["code"], expected["code"])
            self.assertEqual(res["msg"], expected["msg"])
            if item["title"] == "审核通过":
                TestAudit.pass_project_id = params["loan_id"]
            if sql:
                res = db.find_data(sql.format(self.project_id))
                status = res[0]["status"]
                self.assertEqual(status,expected["status"])
        except AssertionError as e:
            log.error("用例执行失败：{}".format(item["title"]))
            log.exception(e)
            self.excel_audit.write_data(row=case_id + 1, column=8, value="失败")
            raise e
        else:
            log.info("用例执行通过：{}".format(item["title"]))
            self.excel_audit.write_data(row=case_id + 1, column=8, value="通过")

