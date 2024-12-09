from src.utils.decorators import exception_catcher as ec
from src.utils.decorators import logger
from src.utils.logger import log


class Login:
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
            self.bt_phone_log = page.locator("text = 手机验证码登录")

        except Exception as e_locator:
            log.error(f"元素定位错误{e_locator}")
            pass

    @logger
    @ec
    def username_input(self):
        """输入用户名"""
        return self.input_username.fill("admin")

    @logger
    @ec
    def password_input(self):
        """输入密码"""
        return self.input_password.fill("xz666666")

    @logger
    @ec
    def login_click(self):
        """点击登录"""
        return self.bt_login.click()
