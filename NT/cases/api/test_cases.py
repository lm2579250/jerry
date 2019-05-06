import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage
from NT.common.send_request import SendRequest


class APITestCases(unittest.TestCase):
    """api请求类"""

    def setUp(self):
        self.request = SendRequest()
        self.base_page = BasePage()
        self.log = MyLog.get_log().logger

    def execute_case(self, case_params, case_num, case_name):
        """api请求实现"""
        try:
            # 从用例中提取负责人姓名
            principal = case_params["principal"]
            # 用例开始头部信息
            self.base_page.case_start(principal, case_name, case_num)
            # 期望返回的文本内容和状态码
            msg, code = "", ""

            self.log.info("用例参数：%s" % case_params)
            for param_key, param_value in case_params.items():
                if param_key == "msg":
                    msg = param_value
                if param_key == "code":
                    code = int(param_value)

            # 发起请求
            response = self.request.send_request(case_params)

            self.log.debug("是否请求成功：%s" % response.ok)  # 查看response.ok的布尔值判断是否请求成功
            self.log.debug("返回状态码：%s" % response.status_code)  # 失败请求(非200响应)抛出异常
            self.log.debug("接口响应时长：%s s" % response.elapsed.total_seconds())
            self.log.debug("当前编码：%s" % response.encoding)
            self.log.debug("请求的url：%s" % response.url)
            self.log.debug("请求返回json：%s" % response.json())
            self.log.debug("请求头：%s" % response.request.headers)  # 发送到服务器的头信息
            self.log.debug("响应头：%s" % response.headers)  # 以字典对象存储服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在则返回None
            # self.log.debug(response.history)  # 返回重定向信息,当然可以在请求时加上allow_redirects = false 阻止重定向
            # self.log.debug(response.raw.read())  # 返回原始响应体，也就是 urllib 的 response 对象，使用 r.raw.read()
            # self.log.debug(response.content)  # 以字节形式（二进制）返回，中文显示为字符。字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩
            # self.log.debug("cookies：%s" % response.cookies)
            # sid = jsonpath(response.json(), '$..sid')  # sid = jsonpath(req, '$..sid')[0]
            # self.log.debug("sid：%s" % sid)

            # 断言
            tip = response.json()["tip"]
            actual_code = response.json()["code"]
            self.assertEqual(msg, tip, "msg期望值：%s，实际值%s" % (msg, tip))
            self.assertEqual(code, actual_code, "code期望值：%s，实际值%s" % (code, actual_code))

            response.raise_for_status()  # 状态码不是200时抛出异常
            self.base_page.case_pass()
        except Exception as e:
            self.log.error("%s" % e)
            self.base_page.case_failed()
            raise Exception
        finally:
            self.base_page.case_end()

    def test_login_controller1(self):
        """用户名和密码都正确"""
        case_params = {'principal': '乔一庭', 'remark': '用户名和密码都正确', 'method': 'post', 'url': '/web/login', 'params': '{"username": "hctest", "password": "hctest"}', 'msg': '成功', 'code': 1}
        case_num = 1
        case_name = 'login_controller1'

        APITestCases.execute_case(self, case_params, case_num, case_name)

    def test_login_controller2(self):
        """用户名和密码都不正确"""
        case_params = {'principal': '吴斌', 'remark': '用户名和密码都不正确', 'method': 'post', 'url': '/web/login', 'params': '{"username": "hctest0", "password": "hctest0"}', 'msg': '用户不存在', 'code': 0}
        case_num = 2
        case_name = 'login_controller2'

        APITestCases.execute_case(self, case_params, case_num, case_name)

    def test_login_controller3(self):
        """密码正确用户名错误"""
        case_params = {'principal': '张跃鑫', 'remark': '密码正确用户名错误', 'method': 'post', 'url': '/web/login', 'params': '{"username": "hctest0", "password": "hctest"}', 'msg': '用户不存在', 'code': 0}
        case_num = 3
        case_name = 'login_controller3'

        APITestCases.execute_case(self, case_params, case_num, case_name)

    def test_login_controller4(self):
        """用户名正确密码错误"""
        case_params = {'principal': '李彬', 'remark': '用户名正确密码错误', 'method': 'post', 'url': '/web/login', 'params': '{"username": "hctest", "password": "hctest0"}', 'msg': '用户名或密码错误', 'code': 0}
        case_num = 4
        case_name = 'login_controller4'

        APITestCases.execute_case(self, case_params, case_num, case_name)

    def test_login_controller5(self):
        """文件上传"""
        case_params = {'principal': '李彬', 'remark': '文件上传', 'method': 'post', 'url': None, 'params': 'D:\\\\test_data\\\\summer_test_data_05.txt', 'msg': None, 'code': None}
        case_num = 5
        case_name = 'login_controller5'

        APITestCases.execute_case(self, case_params, case_num, case_name)

