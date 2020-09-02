'''
项目结构说明:
    common:存放一些自己封装的公共模块（修改源码的ddt)
    data:存放excel文件的用例数据
    logs:存放日志文件
    report:存放测试报告
    testcase:存放测试用例模块
    run.py:项目的启动文件

    funcs(实际项目中不需要)这是用例被测的功能函数的

存在的问题：
1.项目里面用了很多的绝对路径，项目没办法直接移植到别的电脑上跑
优化项目中的路径: 
            os.path.abspath
            os.path.dirname
            os.path.join
2.项目的可配置性不强
添加配置文件： ini,conf,cfg

配置块:select
配置项:option
'''

import os

# 项目的根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试用例的目录路径
CASE_DIR = os.path.join(BASE_DIR,'testcase')
# 测试报告目录的路径
REPORT_DIR = os.path.join(BASE_DIR,'reports')
# 日志目录的目录路径
LOG_DIR = os.path.join(BASE_DIR,'logs')
# 用例数据的目录路径
DATA_DIR = os.path.join(BASE_DIR,'data')
# 配置文件的目录路径
CONF_DIR= os.path.join(BASE_DIR,'conf')

print(LOG_DIR)




