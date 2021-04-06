import logging
import random
import unittest
import requests

import app
from api.LoginAPI import LoginAPI
from api.TrustAPI import TrustAPI
from utils import assert_utils, third_part_request
from bs4 import BeautifulSoup


class TestTrust(unittest.TestCase):
    # 初始化方法
    def setUp(self) -> None:
        # 初始化接口API对象
        self.login_api = LoginAPI()
        self.trust_api = TrustAPI()
        # 初始化session对象
        self.session = requests.Session()

    # 结束方法
    def tearDown(self) -> None:
        self.session.close()

    # 开户
    def test01_trust_register(self):
        # 1、登录操作
        response = self.login_api.login(self.session,app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        # 2、发送开户请求
        # 准备测试数据
        # 调用接口API方法发送请求，并接收响应
        response = self.trust_api.trust_register(self.session)
        logging.info("trust response = {}".format(response.json()))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        html_data = response.json().get("description").get("form")
        # 3、发送开户请求到第三方接口
        response = third_part_request(html_data)
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual("UserRegister OK",response.text)

    # 充值
    def test02_recharge(self):
        # 1、登录
        response = self.login_api.login(self.session,app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、获取充值验证码
        r_data = random.random()
        response = self.trust_api.get_recharge_code(self.session,str(r_data))
        logging.info("get recharge code response = {}".format(response.text))
        self.assertEqual(200,response.status_code)
        # 3、充值请求
        amount = '1000'
        response = self.trust_api.recharge(self.session,amount)
        logging.info("recharge response = {}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        # 4、第三方充值请求
        # 准备测试数据
        html_data = response.json().get("description").get("form")
        # 调用封装的第三方请求的方法
        response = third_part_request(html_data)
        logging.info("third_part recharge response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual("NetSave OK",response.text)