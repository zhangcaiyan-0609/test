import requests
from common.handle_config import conf
from common.handle_path import CONF_DIR
from common.handle_db import db
import random
from jsonpath import jsonpath
def random_phone():
    while True:
        phone = "176"
        for i in range(0,8):
            i = random.randint(0,9)
            phone += str(i)
        sql = "SELECT * FROM futureloan.member WHERE mobile_phone ={}".format(phone)
        res = db.find_data(sql)
        if not res:
            return phone
def register(user_conf,pwd_conf,type=1):
    headers = eval(conf.get("env", "headers"))
    url = conf.get("env", "base_url") + "/member/register"
    params = {
        "mobile_phone": random_phone(),
        "pwd": "12345678",
        "type": type}
    response = requests.post(url=url, json=params, headers=headers)
    mobile = str(params["mobile_phone"])
    pwd = str(params["pwd"])
    conf.write_data("test_data", user_conf, mobile)
    conf.write_data("test_data", pwd_conf, pwd)
    return mobile,pwd

def login(mobile,pwd):
    login_url = conf.get("env", "base_url") + "/member/login"
    login_params = {
        "mobile_phone":mobile,
        "pwd":pwd
    }
    headers = eval(conf.get("env","headers"))
    login_response = requests.post(url=login_url, json=login_params, headers=headers)

    member_id = jsonpath(login_response.json(), "$..id")[0]
    token = "Bearer" + " " + jsonpath(login_response.json(), "$..token")[0]
    return member_id,token
def recharge(token,member_id,money=500000):
    headers = eval(conf.get("env","headers"))
    headers["Authorization"] = token
    recharge_url = conf.get("env", "base_url") + "/member/recharge"
    recharge_params = {"member_id": member_id,"amount": money}
    recharge_response = requests.request(url=recharge_url, method="post", json=recharge_params, headers=headers)

def init_env_data():
    #  注册普通用户（借款人），并保存到配置文件
    user_info = register(user_conf="mobile",pwd_conf="pwd")
    # 注册普通用户（投资人），并保存到配置文件
    user2 = register(user_conf="invest_mobile",pwd_conf="invest_pwd")
    # 注册管理员，并保存到配置文件
    register(user_conf="admin_mobile",pwd_conf="admin_pwd",type=0)

    # 借款人提取用户ID，token
    member_id,token = login(*user_info)
    # 给用户充值
    recharge(token,member_id)
    recharge(token,member_id)
    # 投资人登录 获取用户ID
    member_id2,token2 = login(*user2)
    # 给用户充值
    recharge(token2,member_id2)
    recharge(token2,member_id2)
