import unittest

from script.TestApprove import TestApprove
from script.TestLogin import TestLogin
from script.TestTrust import TestTrust
from script.tender import tender
from script.tender_process import test_tender_process

import app,time
from lib.HTMLTestRunner_PY3 import HTMLTestRunner

# 1、创建测试套件
suite = unittest.TestSuite()
# 2、将编写的测试脚本添加到测试套件
suite.addTest(unittest.makeSuite(TestLogin))
suite.addTest(unittest.makeSuite(TestApprove))
suite.addTest(unittest.makeSuite(TestTrust))
suite.addTest(unittest.makeSuite(tender))
suite.addTest(unittest.makeSuite(test_tender_process))
# 3、执行测试套件，并生成测试报告
#report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d_%H%M%S"))
report_file = app.BASE_DIR + "/report/report.html"

with open(report_file,'wb') as f:
    runner = HTMLTestRunner(f,title="金融项目接口自动化测试报告",description="BJ27 Python+Requests")
    runner.run(suite)