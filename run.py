import unittest
from unittestreport import TestRunner

import os
from common.handle_path import CASE_DIR,REPORT_DIR
from common.handle_config import conf
from tools.tools import init_env_data

# 第一步：创建一个测试套件
suite = unittest.TestSuite()
# 第二步：将测试用例添加到测试套件中
# 2.1 创建加载器
loader = unittest.TestLoader()
# 2.2 加载用例到套件
suite.addTest(loader.discover(CASE_DIR))

# 准备一些测试的环境数据
init_env_data()
# 第三步：执行测试用例
# 方式一
runner = TestRunner(suite, filename = conf.get('report','filename'), report_dir= REPORT_DIR,title='caiyan项目框架测试报告',tester='caiyan',desc='caiyan执行的测试')
runner.run()
# 执行后发送邮件
print("发送邮件")
runner.send_email(host="smtp.qq.com",
                  port=465,
                  user="441583097@qq.com",
                  password="yowycaqxkzrjbiji",
                  to_addrs=["caiyanyifei@163.com","zhangcaiyan@jd.com"])

print("发送邮件成功")
# 授权码：yowycaqxkzrjbiji