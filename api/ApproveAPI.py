import app


class ApproveAPI(object):
    # 定义初始化的方法
    def __init__(self):
        self.approve_url = app.BASE_URL + "/member/realname/approverealname"
        self.get_approve_url = app.BASE_URL + "/member/member/getapprove"

    # 定义认证接口请求
    def approve(self,session,realname,card_id):
        # 准备测试数据
        data = {"realname":realname,
                "card_id":card_id}
        # 发送请求，并接收响应
        response = session.post(self.approve_url,data=data,files={"x":"y"})
        # 返回响应
        return response

    # 获取认证信息
    def get_approve(self,session):
        # 准备测试数据
        # 发送请求，并接收响应
        response = session.post(self.get_approve_url)
        # 返回响应
        return response