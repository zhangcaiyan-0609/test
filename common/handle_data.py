import re
from common.handle_config import conf
class EnvData:
    member_id = 123
    user ="cathy"
    loan = 31
def replace_data(data,cls):
    
    while re.search("#(.+?)#",data):
        item = re.search("#(.+?)#",data)
        #需要替换的数据
        rep_data = item.group()
        #要替换的类属性
        key = item.group(1)
        try:
            value = conf.get("test_data",key)
        except:
            value = getattr(cls,key)
        data = data.replace(rep_data,str(value))
    return data

