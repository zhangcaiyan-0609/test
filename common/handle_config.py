from configparser import ConfigParser
from common.handle_path import CONF_DIR
import os
class Config(ConfigParser):
    def __init__(self,filename,encoding='utf-8'):
        super().__init__()
        self.read(filename,encoding='utf-8')
        self.filename = filename
        self.encoding = encoding

    def write_data(self,select,option,value):
        # 往配置文件写入数据
        self.set(select,option,value)
        self.write(fp=open(self.filename,"w",encoding=self.encoding))

# 创建一个配置文件解析器
conf = Config(os.path.join(CONF_DIR,"config.ini"))


