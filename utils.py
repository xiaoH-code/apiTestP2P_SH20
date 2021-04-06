import json
import logging
from logging import handlers
import pymysql
import requests
from bs4 import BeautifulSoup

import app


# 初始化日志配置
def init_log_config():
    # 1、创建日志对象
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 2、创建控制台处理器和文件处理器
    sh = logging.StreamHandler()

    log_file = app.BASE_DIR + "/log/p2p.log"
    fh = logging.handlers.TimedRotatingFileHandler(log_file, when='M', interval=5, backupCount=3,encoding='UTF-8')
    # 3、创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)

    # 4、将格式化器添加到控制器处理和文件处理器
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 5、将控制台处理器和文件处理器绑定到日志
    logger.addHandler(sh)
    logger.addHandler(fh)


# 定义断言的公共函数
def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))

# 发送第三方请求
def third_part_request(html_data):
    # 3、发送开户请求到第三方接口
    # 准备测试数据
    soup = BeautifulSoup(html_data, "html.parser")
    # 从响应数据中提取url
    third_request_url = soup.form["action"]
    # 从响应数据中提取参数数据
    data = {}
    for input in soup.find_all("input"):
        data.setdefault(input["name"], input["value"])
    # 发送请求，并接收响应
    response = requests.post(third_request_url, data=data)
    logging.info("third-request reponse = {}".format(response.text))
    return response

# 连接数据库的类
class DButils(object):
    @classmethod
    def get_conn(cls):
        conn = pymysql.Connect(user='root',password='Itcast_p2p_20191228',host='admin-p2p-test.itheima.net',database='czbk_member',port=3306,charset='utf8',autocommit=True)
        return conn

    @classmethod
    def close_conn(cls,cursor,conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def execute_sql(cls,sql):
        try:
            # 建立连接
            conn = cls.get_conn()
            # 创建游标
            cursor = conn.cursor()
            # 执行sql
            cursor.execute(sql)
        finally:
            # 关闭游标和关闭连接
            cls.close_conn(cursor,conn)

# 读取图片验证码的参数化数据文件
def read_imgCode_data():
    # 获取参数化文件
    file_path = app.BASE_DIR + '/data/imgCode.json'
    # 定义空列表
    test_case_list = []
    # 打开文件，循环读取数据内容
    with open(file_path,encoding='utf-8') as f:
        # 将json格式的数据转换为字典格式的数据
        dict_data = json.load(f)
        # 循环读取参数化文件的数据
        for test_case in dict_data:
            data = test_case.get("data_type")
            status_code = test_case.get("status_code")
            test_case_list.append((data,status_code))
    return test_case_list

# 读取注册参数化数据文件
def read_register_data():
    # 获取参数化文件
    file_path = app.BASE_DIR + "/data/register.json"
    # 定义空列表
    test_case_list = []
    # 打开文件，循环读取数据内容
    with open(file_path,encoding='utf-8') as f:
        # 将json文件转换为字典格式
        dict_data = json.load(f)
        # 循环读取参数化文件中的数据
        for test_case in dict_data:
            data = test_case.get("data")
            status_code = test_case.get("status_code")
            status = test_case.get("status")
            desc = test_case.get("desc")
            test_case_list.append((data,status_code,status,desc))
    return test_case_list

# 读取参数化的数据文件的测试数据
def read_params_data(filename):
    # 读取参数化文件
    file_path = app.BASE_DIR + "/data/" + filename
    # 定义空列表
    test_case_list = []
    # 打开文件，循环读取数据内容
    with open(file_path,encoding='utf-8') as f:
        # 将json文件转换为字典格式
        dict_data = json.load(f)
        # 循环读取参数化文件中的数据
        for test_case in dict_data:
            test_case_list.append(tuple(test_case.values()))
    return test_case_list