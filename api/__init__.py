from utils import init_log_config
import logging

# 初始化日志函数
init_log_config()
# 调用日志打印函数来输出日志
logging.error("1、这是一个error日志")
logging.info("2、这是一个info日志")
logging.debug("3、这是一个debug日志")
print("4、这是一个print日志")