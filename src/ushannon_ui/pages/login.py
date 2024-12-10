from src.utils.decorators import exception_catcher as ec
from src.utils.decorators import logger
from src.utils.logger import log


class LoginPage(object):
    def __init__(self, page):
        self.page = page

        try:
            # 初始化元素
            # 用户名输入框
            self.input_username = self.page.locator("#username")
            # 密码输入框
            self.input_password = self.page.locator("#password")
            # 登录按钮
            self.bt_login = self.page.locator("[type = submit]")
            # 切换手机号登录按钮
            self.bt_phone_log = self.page.locator("text = 手机验证码登录")
            # 用户协议复选框
            self.cb_agreement = self.page.locator(".semi-checkbox-inner-display")
            # 跳转网页：1.用户协议；2.隐私政策；3.备案网页1；4.备案网页2
            self.a = self.page.locator("div a")

        except Exception as e_locator:
            log.error(f"元素定位错误{e_locator}")

    @logger
    @ec
    def username_input(self, content: str):
        """输入用户名"""
        return self.input_username.fill(content)

    @logger
    @ec
    def password_input(self, content: str):
        """输入密码"""
        return self.input_password.fill(content)

    @logger
    @ec
    def agreement_click(self):
        """勾选用户协议"""
        return self.cb_agreement.click()

    @logger
    @ec
    def login_click(self):
        """点击登录"""
        return self.bt_login.click()

    @logger
    @ec
    def a_goto(self, nth):
        """前往用户协议网页"""
        return self.a.nth(nth).click()
