# 需求：在执行的过程中，记录日志(把日志记录到文件)
# 封装一个创建日志收集器的方法
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from common.handle_path import LOG_DIR
from common.handle_config import conf
file_path = os.path.join(LOG_DIR,conf.get('logging','log_name'))

def create_logger():

    # 1 创建一个收集器
    log = logging.getLogger('cathy')
    # 设置收集日志的等级
    log.setLevel(conf.get("logging",'level'))
    # 2 创建一个输出到文件的输出渠道(按时间轮转)
    fh = TimedRotatingFileHandler(file_path,when='d',interval=1,backupCount=7,encoding='utf-8')
    # 3 设置输出等级
    fh.setLevel(conf.get("logging","fh"))
    # 4 添加到收集器中
    log.addHandler(fh)

    # 5 创建一个输出到控制台的输出渠道
    sh = logging.StreamHandler()
    sh.setLevel(conf.get('logging','sh'))
    log.addHandler(sh)
    # 设置日志输出格式
    formats = "%(asctime)-15s %(levelname)s [%(filename)s %(lineno)d] %(message)s"
    mate = logging.Formatter(formats)
    sh.setFormatter(mate)
    fh.setFormatter(mate)
    return log

log = create_logger()




