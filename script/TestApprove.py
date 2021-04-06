import logging
import unittest
import requests

import app
from api.ApproveAPI import ApproveAPI
from api.LoginAPI import LoginAPI
from utils import assert_utils


class TestApprove(unittest.TestCase):
    # 初始化方法
    def setUp(self) -> None:
        # 初始化接口类对象
        self.login_api = LoginAPI()
        self.approve_api = ApproveAPI()
        # 初始化session对象
        self.session = requests.Session()
        # 初始化测试数据
        self.realname = "张三"
        self.card_id = "410482198305221584"

    # 结束方法
    def tearDown(self) -> None:
        # 关闭session对象
        self.session.close()

    # 输入正确的姓名和身份证号，认证成功
    def test01_approve_success(self):
        # 1、登录操作
        response = self.login_api.login(self.session,app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        # 2、认证操作
        # 准备测试数据
        # 调用API方法发送请求，接收响应
        response = self.approve_api.approve(self.session,self.realname,self.card_id)
        logging.info("response = {}".format(response.json()))
        # 对响应进行断言
        assert_utils(self,response,200,200,"提交成功!")

    # 姓名为空，认证失败
    def test02_approve_fail_realname_is_null(self):
        # 1、登录操作
        response = self.login_api.login(self.session,app.phone2)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        # 2、认证操作
        # 准备测试数据
        # 调用API方法发送请求，接收响应
        response = self.approve_api.approve(self.session,"",self.card_id)
        logging.info("response = {}".format(response.json()))
        # 对响应给结果进行断言
        assert_utils(self,response,200,100,"姓名不能为空")

    # 身份证号为空，认证失败
    def test03_approve_fail_cardid_is_null(self):
        # 1、登录操作
        response = self.login_api.login(self.session,app.phone2)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        # 2、认证操作
        # 准备测试数据
        # 调用API方法发送请求，接收响应
        response = self.approve_api.approve(self.session,self.realname,"")
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"身份证号不能为空")

    # 获取认证信息
    def test04_get_approve(self):
        # 1、登录操作
        response = self.login_api.login(self.session,app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        # 2、获取认证
        # 准备测试数据
        # 调用API方法发送请求，接收响应
        response = self.approve_api.get_approve(self.session)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual("410****584",response.json().get("card_id"))