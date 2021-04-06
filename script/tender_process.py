import logging
import random

import requests,unittest

import app
from api.LoginAPI import LoginAPI
from api.tenderAPI import tenderAPI
from api.TrustAPI import TrustAPI
from utils import assert_utils, third_part_request,DButils

class test_tender_process(unittest.TestCase):
    tender_id = app.tender_id
    imVerifyCode = '8888'
    phone = app.phone5

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = LoginAPI()
        cls.tender_api = tenderAPI()
        cls.trust_api = TrustAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        sql1 = "DELETE i.* from czbk_member.mb_member_info i INNER JOIN czbk_member.mb_member m ON i.member_id = m.id WHERE m.phone in ('{}','{}','{}','{}','{}');"
        DButils.execute_sql(sql1.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("执行清理数据的sql语句为：{}".format(sql1.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))
        sql2 = "DELETE i.* from czbk_member.mb_member_info i INNER JOIN czbk_member.mb_member m ON i.member_id = m.id WHERE m.phone in ('{}','{}','{}','{}','{}');"
        DButils.execute_sql(sql2.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("执行清理数据的sql语句为：{}".format(sql2.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))
        sql3 = "DELETE f.* from czbk_finance.fn_tender f INNER JOIN czbk_member.mb_member m on f.member_id = m.id WHERE m.phone in ('{}','{}','{}','{}','{}');"
        DButils.execute_sql(sql3.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("执行清理数据的sql语句为：{}".format(sql3.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))
        sql4 = "DELETE from czbk_member.mb_member_register_log  WHERE phone in ('{}','{}','{}','{}','{}');"
        DButils.execute_sql(sql4.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("执行清理数据的sql语句为：{}".format(sql4.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))
        sql5 = "DELETE from czbk_member.mb_member where phone in ('{}','{}','{}','{}','{}');"
        DButils.execute_sql(sql5.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("执行清理数据的sql语句为：{}".format(sql5.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))

    def test01_register_success(self):
        # 请求图片验证码
        r = random.random()
        response = self.login_api.get_img_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.get_sms_verify_code(self.session, self.phone, self.imVerifyCode)
        logging.info("sms verify response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.register(self.session, self.phone, 'test123')
        logging.info("reg response={}".format(response.json()))
        # 断言
        assert_utils(self, response, 200, 200, "注册成功")

    def test02_login_success(self):
        """登录成功"""
        #发送登录请求
        response = self.login_api.login(self.session,self.phone, 'test123')
        logging.info("login response={}".format(response.json()))
        #断言
        assert_utils(self,response,200,200,"登录成功")

    def test03_trust_success(self):
        """开户"""
        #获取开户信息
        response = self.trust_api.trust_register(self.session)
        logging.info("trust response={}".format(response.json()))
        #断言获取的开户信息是否正确
        self.assertEqual(200,response.status_code)
        self.assertEqual(200, response.json().get("status"))
        #获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        #发送第三方的请求，请求第三方接口进行开户
        response = third_part_request(form_data)
        logging.info("third-interface response={}".format(response.text))
        #断言第三方接口请求处理是否成功
        self.assertEqual('UserRegister OK',response.text)

    def test04_recharge_success(self):
        """充值"""
        # 获取充值验证码
        r = random.random()
        response = self.trust_api.get_recharge_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        logging.info("get_recharge_code response={}".format(response.text))

        # 充值
        amount = '1000'
        response = self.trust_api.recharge(self.session, amount)
        logging.info("recharge response={}".format(response.text))
        # 断言获取的开户信息是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = third_part_request(form_data)
        logging.info("third-interface response={}".format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('NetSave OK', response.text)

    def test05_get_loaninfo(self):
        """获取投资产品详情"""
        #请求投资产品的详情
        response = self.tender_api.get_loaninfo(self.session,self.tender_id)
        logging.info("get_tender response = {}".format(response.json()))
        #断言投资详情是否正确
        assert_utils(self,response,200,200,"OK")
        self.assertEqual(str(self.tender_id),response.json().get("data").get("loan_info").get("id"))

    def test06_tender(self):
        #投资
        #发送投资请求
        amount = '100'
        response = self.tender_api.tender(self.session,self.tender_id,amount)
        logging.info("tender response = {}".format(response.json()))
        #断言投资结果是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = third_part_request(form_data)
        logging.info("third-interface response={}".format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('InitiativeTender OK', response.text)

    def test07_get_tenderlist(self):
        """获取我的投资列表"""
        status = "tender"
        #发送获取投资列表的请求
        response = self.tender_api.get_tenderlist(self.session,status)
        logging.info("get_tender response = {}".format(response.json()))
        self.assertEqual(200,response.status_code)