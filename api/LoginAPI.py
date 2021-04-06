import app


class LoginAPI(object):
    def __init__(self):
        self.get_img_verify_code_url = app.BASE_URL + "/common/public/verifycode1/"
        self.get_sms_verify_code_url = app.BASE_URL + "/member/public/sendSms"
        self.register_url = app.BASE_URL + "/member/public/reg"
        self.login_url = app.BASE_URL + "/member/public/login"
        self.islogin_url = app.BASE_URL + "/member/public/islogin"

    # 定义获取图片验证码的请求接口
    def get_img_verify_code(self, session, r):
        # 准备测试数据
        img_url = self.get_img_verify_code_url + r
        # 发送请求，并接收响应
        response = session.get(img_url)
        # 返回响应
        return response

    # 定义获取短信验证码的请求接口
    def get_sms_verify_code(self,session,phone,imgCode):
        # 准备测试数据
        data = {"phone": phone, "imgVerifyCode": imgCode, "type": "reg"}
        # 发送请求，接收响应
        response = session.post(self.get_sms_verify_code_url,data=data)
        # 返回响应
        return response

    # 定义注册的请求接口
    def register(self,session,phone,pwd="test123",imgCode="8888",phoneCode="666666",dy_Server="on",invitePhone=""):
        # 准备测试数据
        data = {"phone":phone,
                "password":pwd,
                "verifycode":imgCode,
                "phone_code":phoneCode,
                "dy_server":dy_Server,
                "invite_phone":invitePhone}
        # 发送请求，接收响应
        response = session.post(self.register_url,data=data)
        # 返回响应
        return response

    # 定义登录的接口请求
    def login(self,session,phone,pwd="test123"):
        # 准备测试数据
        data = {"keywords":phone,"password":pwd}
        # 发送请求，接收响应
        response = session.post(self.login_url,data=data)
        # 返回响应
        return response

    # 定义验证登录状态的接口请求
    def islogin(self,session):
        # 准备测试数据
        # 发送请求，接收响应
        response = session.post(self.islogin_url)
        # 返回响应
        return response