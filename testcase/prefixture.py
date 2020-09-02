from common.handle_config import conf
from jsonpath import jsonpath
import requests
import random
def setup_login(cls):
    """
    普通用户登录（投资接口中的借款人）
    :param cls:
    :return:
    """
    """
    写该用例类执行之前的前置
    登录，获取token和用户id
    """
    login_url = conf.get("env", "base_url") + "/member/login"
    login_params = {
        "mobile_phone": conf.get("test_data", "mobile"),
        "pwd": conf.get("test_data", "pwd")
    }
    headers = eval(conf.get("env","headers"))
    login_response = requests.post(url=login_url, json=login_params, headers=headers)
    cls.member_id = jsonpath(login_response.json(), "$..id")[0]
    cls.token = "Bearer" + " " + jsonpath(login_response.json(), "$..token")[0]

def setup_login_invest(cls):
    login_url = conf.get("env", "base_url") + "/member/login"
    login_params = {
        "mobile_phone": conf.get("test_data", "invest_mobile"),
        "pwd": conf.get("test_data", "invest_pwd")
    }
    headers = eval(conf.get("env", "headers"))
    login_response = requests.post(url=login_url, json=login_params, headers=headers)
    #  提取投资用户的ID和token
    cls.invest_member_id = jsonpath(login_response.json(), "$..id")[0]
    cls.invest_token = "Bearer" + " " + jsonpath(login_response.json(), "$..token")[0]

def setup_login_admin(cls):
    login_url = conf.get("env", "base_url") + "/member/login"
    login_params = {
        "mobile_phone": conf.get("test_data", "admin_mobile"),
        "pwd": conf.get("test_data", "admin_pwd")
    }
    headers = eval(conf.get("env", "headers"))
    login_response = requests.post(url=login_url, json=login_params, headers=headers)
    #  提取管理员的token
    cls.admin_token = "Bearer" + " " + jsonpath(login_response.json(), "$..token")[0]

def setup_add(cls):
    # 添加项目的前置
    add_url = conf.get("env", "base_url") + "/loan/add"
    headers = eval(conf.get("env", "headers"))
    headers["Authorization"] = cls.token
    params = {
        "member_id": cls.member_id,
        "title": "sun".format(random.randint(0, 100)),
        "amount": 1000,
        "loan_rate": 5.76,
        "loan_term": 6,
        "loan_date_type": 1,
        "bidding_days": 1
    }
    response = requests.request(url=add_url, method="post", json=params, headers=headers)
    res = response.json()
    # 将项目ID保存为类属性
    cls.loan_id = jsonpath(res, "$..id")[0]

