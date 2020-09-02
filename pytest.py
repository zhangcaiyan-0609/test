import requests
from common.handle_config import conf
from jsonpath import jsonpath
login_url = "http://api.lemonban.com/futureloan/member/login"
params = {
    "mobile_phone":conf.get("test_data","admin_mobile"),
    "pwd":conf.get("test_data","admin_pwd")

}

headers ={
    "X-Lemonban-Media-Type": "lemonban.v2"
}

response = requests.post(url=login_url,json=params,headers=headers)
res = response.json()
print(res)
token = "Bearer" + " " + jsonpath(res,"$..token")[0]
print(token)

audit_url = "http://api.lemonban.com/futureloan/loan/audit"

params2 ={"loan_id":1023,"approve_or_not":True}
headers2 = {
    "X-Lemonban-Media-Type": "lemonban.v2",
    "Authorization": token
}
response2 = requests.patch(url=audit_url,json=params2,headers=headers2)
print(response2.json())










