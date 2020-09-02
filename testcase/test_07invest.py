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
from testcase import prefixture
"""
投资的前置条件：
借款人登录
管理员登录
投资人登录

借款人新建项目
管理员审核项目
投资人投资项目
投资：
    前置：需要有一个状态处于竞标中的项目（登录-->添加项目--->审核通过）
        登录--->投资

    借款人：添加项目
    管理员：审核项目
    投资人：投资
    普通用户：既可以借款，又可以投资


用户登录：setupclass:
添加项目：setupclass:
审核项目：setupclass:

用例逻辑中：投资


用例执行完之后，如果数据库中涉及到多张表的数据变动，如何去进行校验
那些表，那字段发送了变化
1、投资表中新增一条数据？--->用例执行前后 根据用户和标id查询投资记录的条数
2、用户表中可用余额减少？--->用例执行前后查数据库中的余额进行比对？
3、流水记录表中新增一条数据？  --->用例执行前后 根据用户id查询流水记录的条数

"""
@myddt.ddt
class TestInvest(unittest.TestCase):
    excel = Excel(os.path.join(DATA_DIR,"cases.xlsx"),"invest")
    cases = excel.read_data()
    @classmethod
    def setUpClass(cls):
        prefixture.setup_login(cls)
        prefixture.setup_login_invest(cls)
        prefixture.setup_login_admin(cls)
        prefixture.setup_add(cls)
        # 审核项目
        audit_url = conf.get("env", "base_url") + "/loan/audit"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = cls.admin_token
        params = {
            "loan_id": cls.loan_id, "approved_or_not": True}
        response = requests.patch(url=audit_url, json=params, headers=headers)
        res = response.json()
    @myddt.data(*cases)
    def test_invest(self,item):
        # 获取用例编号
        case_id = item["case_id"]
        # 请求接口
        url = conf.get("env","base_url") + item["url"]
        # 请求方法
        method = item["method"]
        # 请求头
        headers = eval(conf.get("env","headers"))
        headers["Authorization"] = self.invest_token
        # 请求参数
        item["data"] = replace_data(item["data"],TestInvest)
        params = eval(item["data"])
        # 预期结果
        expected = eval(item["expected"])
        # 用例执行前的数据校验
        if item["check_sql"]:
            # 查询投资表记录
            sql1 = "SELECT * from futureloan.invest WHERE member_id ={} and loan_id = {}".format(self.invest_member_id,self.loan_id)
            # 查询用户的余额
            sql2 = "SELECT * from futureloan.member WHERE id = {}".format(self.invest_member_id)
            # 查询流水记录
            sql3 = "SELECT * from futureloan.financelog WHERE pay_member_id = {}".format(self.invest_member_id)
            # 查询用例执行前投资记录的条数
            s_invest = len(db.find_data(sql1))
            # 查询用例执行前投资用户的余额
            s_amount = db.find_data(sql2)[0]["leave_amount"]
            # 查询用例执行前流水记录表记录的用户的流水记录条数
            s_financelog = len(db.find_data(sql3))

        # 第二步 发送请求
        response = requests.request(url=url,method=method,json=params,headers=headers)
        res = response.json()
        print("实际结果",res)
        print("预期结果",expected)
        # 第三步 断言
        try:
            self.assertEqual(res["code"],expected["code"])
            self.assertEqual(res["msg"],expected["msg"])
            if item["check_sql"]:
                # 查询投资表记录
                sql1 = "SELECT * from futureloan.invest WHERE member_id ={} and loan_id = {}".format(self.invest_member_id, self.loan_id)
                # 查询用户的余额
                sql2 = "SELECT * from futureloan.member WHERE id = {}".format(self.invest_member_id)
                # 查询流水记录
                sql3 = "SELECT * from futureloan.financelog WHERE pay_member_id = {}".format(self.invest_member_id)
                # 查询用例执行后投资记录的条数
                e_invest = len(db.find_data(sql1))
                # 查询用例执行后用户的余额
                e_amount = db.find_data(sql2)[0]["leave_amount"]
                # 查询用例执行后流水记录表记录的用户的流水记录条数
                e_financelog = len(db.find_data(sql3))
                # 断言比对
                self.assertEqual(1,e_invest - s_invest)
                self.assertEqual(1,e_financelog - s_financelog)
                self.assertEqual(params["amount"],float(s_amount - e_amount))

        except AssertionError as e:
            log.error("用例执行失败：{}".format(item["title"]))
            log.exception(e)
            self.excel_audit.write_data(row=case_id + 1, column=8, value="失败")
            raise e
        else:
            log.info("用例执行通过：{}".format(item["title"]))
            self.excel.write_data(row=case_id+1,column=8,value="通过")

