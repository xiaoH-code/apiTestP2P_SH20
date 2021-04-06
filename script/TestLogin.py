import time
import unittest
import requests
import random
from api.LoginAPI import LoginAPI
import logging
import app
from utils import assert_utils, DButils


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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

    # 初始化setup
    def setUp(self) -> None:
        # 初始化session对象
        self.session = requests.Session()
        # 初始化接口类对象
        self.login_api = LoginAPI()

    # 结束teardown
    def tearDown(self) -> None:
        # 关闭session对象
        self.session.close()

    # 参数为随机小数时，获取图片验证码成功
    def test01_get_img_code_success_random_float(self):
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)

    # 参数为随机整数时，获取图片验证码成功
    def test02_get_img_code_success_random_int(self):
        # 准备测试数据
        r = random.randint(1000000,9999999)
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)

    # 参数为空，获取图片验证码失败
    def test03_get_img_code_fail_param_is_null(self):
        # 准备测试数据
        r = ''
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,r)
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(404,response.status_code)

    # 参数为随机字母时，获取图片验证码失败
    def test04_get_img_code_fail_random_char(self):
        # 准备测试数据
        r = random.sample('abcdefghijklmn',8)
        str_r = ''.join(r)
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str_r)
        logging.info("str_r = {}".format(str_r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(400,response.status_code)

    # 参数正确时，获取短信验证码成功
    def test05_get_sms_code_success_param_is_true(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone1,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")

    # 图片验证码错误，获取短信验证码失败
    def test06_get_sms_code_fail_img_code_is_wrong(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        wrong_code = '1234'
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone1,wrong_code)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    # 手机号为空，获取短信验证码失败
    def test07_get_sms_code_fail_phone_is_null(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,"",app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))

    # 图片验证码为空，获取短信验证码失败
    def test08_get_sms_code_fail_phone_code_is_null(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone1,"")
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    # 填写必填参数，注册成功
    def test09_register_success_param_is_must(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone1,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.register(self.session,app.phone1)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"注册成功")

    # 填写所有参数，注册成功
    def test10_register_success_all_param(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone2,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.register(self.session,app.phone2,invitePhone="13012345678")
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"注册成功")

    # 图片验证码错误，注册失败
    def test11_register_fail_imgCode_is_wrong(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone3,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.register(self.session,app.phone3,imgCode="1234")
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"验证码错误!")

    # 短信验证码错误，注册失败
    def test12_register_fail_sms_code_is_wrong(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone3,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.register(self.session,app.phone3,phoneCode="123456")
        logging.info("response = {}".format(response.json()))
        # 对响应给结果进行断言
        assert_utils(self,response,200,100,"验证码错误")

    # 手机号已存在，注册失败
    def test13_register_fail_phone_is_exist(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone1,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.register(self.session,app.phone1)
        logging.info("response = {}".format(response.json()))
        # 对响应给结果进行断言
        assert_utils(self,response,200,100,"手机已存在!")

    # 密码为空时，注册失败
    def test14_register_fail_password_is_null(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone3,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口API方法，发送器星期并接收响应
        response = self.login_api.register(self.session,app.phone3,pwd="")
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    # 不同意协议，注册失败
    def test15_register_fail_no_permission_protcol(self):
        # 1、获取图片验证码
        # 准备测试数据
        r = random.random()
        # 调用接口类中定义的方法，发送请求并接收响应
        response = self.login_api.get_img_verify_code(self.session,str(r))
        logging.info("response = {}".format(response.text))
        # 对响应结果进行断言
        self.assertEqual(200,response.status_code)
        # 2、获取短信验证码
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.get_sms_verify_code(self.session,app.phone4,app.imgCode)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        # 3、注册
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.register(self.session,app.phone4,dy_Server="off")
        logging.info("resposne = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"请同意我们的条款")

    # 用户密码正确，登录成功
    def test16_login_success(self):
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"登录成功")

    # 用户名为空，登录失败
    def test17_login_fail_username_is_null(self):
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,"")
        logging.info("resposne = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"用户名不能为空")

    # 用户名未注册，登录失败
    def test18_login_fail_username_is_not_exist(self):
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,"13999882345")
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"用户不存在")

    # 密码为空时，登录失败
    def test19_login_fail_password_is_null(self):
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1,pwd="")
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    # 密码错误时，登录给出错误提示
    def test20_login_fail_password_is_wrong(self):
        # 1、密码错误1次，登录失败
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1,pwd="error")
        logging.info("first-error response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")

        # 2、密码错误2次，登录失败
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1,pwd="error")
        logging.info("second-error response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"密码错误2次,达到3次将锁定账户")

        # 3、密码错误3次，登录失败
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1,pwd="error")
        logging.info("third-error response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        # 4、一分钟内输入正确的用户名密码，登录失败
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1)
        logging.info("1分钟内的响应：{}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        # 5、 一分钟后输入正确的用户名密码，登录成功
        # 准备测试数据
        # 等待一分钟
        time.sleep(60)
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1)
        logging.info("1分钟后的响应：{}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"登录成功")

    # 已登录时，查询当前登录状态
    def test21_islogin_login(self):
        # 1、完成登录
        # 准备测试数据
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.login(self.session,app.phone1)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"登录成功")
        # 2、查询登录状态
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.islogin(self.session)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,200,"OK")

    # 未登录时，查询当前登录状态
    def test22_islogin_no_login(self):
        # 调用接口API方法，发送请求并接收响应
        response = self.login_api.islogin(self.session)
        logging.info("response = {}".format(response.json()))
        # 对响应结果进行断言
        assert_utils(self,response,200,250,"您未登陆！")