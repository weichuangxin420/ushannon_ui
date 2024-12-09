from config.env import URLDve
from utils.logger import log
from utils.decorators import logger,exception_catcher as ec



class LoginPage:

    def __init__(self, page):
        self.page = page

        try:
            #元素初始化
            #用户名输入框
            self.input_username = self.page.locator("[type = text]")
            #密码输入框
            self.input_password = self.page.locator("[type = password]")
            #登录按钮
            self.button_login = self.page.locator("[type = submit]")
            #备案
            self.filing  =


        except Exception as e_login:
            log.error(f"元素定位时发送异常:{self.input_username}")
            raise e_login




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
        return self.button_login.click()


















