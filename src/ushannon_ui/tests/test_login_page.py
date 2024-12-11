import time

import pytest

from config.env import URLDve
from src.utils.random_data_maker import  random_data_maker as rdm
from random import randint

from utils.logger import log


@pytest.mark.usefixtures("init_page")
class TestLogin:

    def test_login(self, login_page):
        """测试登录"""
        login_page[0].value_input({"username":"admin", "password":"xz666666"})
        login_page[0].bt_click("agreement")
        login_page[0].bt_click("login")

        try:
            login_page[2].wait_for_url(
                "https://dev-learn.u-shannon.com/", timeout=10000
            )
            assert True
        except TimeoutError:
            assert False, "超时未跳转到指定url"

            #由于登录后进入了主页，影响其他用例执行，需要返回登录页
        finally:

            # 清除 LocalStorage ，其中包含了token
            login_page[2].evaluate("localStorage.clear();")
            login_page[2].goto(URLDve.OJ_front)


    @pytest.mark.parametrize("values,number",[
        (rdm(11,False,True,True,True),"1"),
        (rdm(randint(0,10),True,False,False,False),"2"),
        (rdm(12,True,False,False,False),"3"),
        (rdm(11,True,False,False,False),"4"),
    ],ids = ["输入非数字字符","输入11以下的数字","输入12位数字","输入11位数字"])
    def test_input(self,login_page,values,number):
        """测试输入框输入"""
        #如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login"):
            login_page[0].bt_click("phone_login")
        login_page[0].value_input({"phone_number":values})
        if number == "1":
            assert login_page[0].get_value("phone_number") == ""
        if number == "2":
            assert login_page[0].get_value("phone_number") == values
        if number == "3":
            assert login_page[0].get_value("phone_number") == values[0:11]
        if number == "4":
            assert login_page[0].get_value("phone_number") == values
        login_page[0].input_clear("phone_number")





class TestGoto:

    @pytest.mark.parametrize(
        "target_url,number",
        [
            ("https://dev-learn.u-shannon.com/userAgreement.html", "0"),
            ("https://dev-learn.u-shannon.com/privacyPolicy.html", "1"),
            ("https://beian.miit.gov.cn/", "2"),
            ("https://beian.mps.gov.cn/#/query/webSearch", "3"),
        ],
    )
    def test_goto(self, login_page, target_url, number):
        """测试跳转"""
        org_page = login_page[2]
        with login_page[1].expect_page() as new_pages:
            login_page[0].a_goto(int(number))
        if new_pages:
            assert target_url in new_pages.value.url
        else:
            assert False, "new_pages 为空"
        org_page.bring_to_front()




