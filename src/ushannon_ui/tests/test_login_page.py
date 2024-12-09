import time
from random import randint

import pytest

from config.env import URLDve
from src.utils.random_data_maker import random_data_maker as rdm
from utils.logger import log


class TestLogin:

    def test_login(self, login_page):
        """测试登录"""
        login_page[0].value_input({"username": "admin", "password": "xz666666"})
        login_page[0].bt_click("agreement")
        login_page[0].bt_click("login")

        try:
            login_page[2].wait_for_url(
                "https://dev-learn.u-shannon.com/", timeout=10000
            )
            assert True
        except TimeoutError:
            assert False, "超时未跳转到指定url"

            # 由于登录后进入了主页，影响其他用例执行，需要返回登录页
        finally:

            # 清除 LocalStorage ，其中包含了token
            login_page[2].evaluate("localStorage.clear();")
            login_page[2].goto(URLDve.OJ_front)

    @pytest.mark.parametrize(
        "values,number",
        [
            (rdm(11, False, True, True, True), "1"),
            (rdm(randint(0, 10), True, False, False, False), "2"),
            (rdm(12, True, False, False, False), "3"),
            (rdm(11, True, False, False, False), "4"),
        ],
        ids=["输入非数字字符", "输入11以下的数字", "输入12位数字", "输入11位数字"],
    )
    def test_phone_input(self, login_page, values, number):
        """测试输入框输入"""
        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login"):
            login_page[0].bt_click("phone_login")
        login_page[0].value_input({"phone_number": values})
        if number == "1":
            assert login_page[0].get_value("phone_number") == ""
        if number == "2":
            assert login_page[0].get_value("phone_number") == values
        if number == "3":
            assert login_page[0].get_value("phone_number") == values[0:11]
        if number == "4":
            assert login_page[0].get_value("phone_number") == values
        login_page[0].input_clear("phone_number")

    @pytest.mark.parametrize(
        "phone_number,number",
        [("17102108412", "1"), ("14000200000", "2"), ("17102108412", "3")],
        ids=["无网获取验证码", "手机号未注册", "成功发送,倒计时后重新发送"],
    )
    def test_get_verifycode(self, login_page, phone_number, number):
        """测试手机号输入框"""

        # 每次执行恢复网络
        login_page[1].set_offline(False)
        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")
        # 输入手机号
        login_page[0].value_input({"phone_number": phone_number})

        # 断言断网吐司
        if number == "1":
            login_page[1].set_offline(True)
            login_page[0].bt_click("get_verifycode")
            assert login_page[0].query_element(
                element="neterror", mode="wait_for_visible"
            )

        if number == "2":
            login_page[0].bt_click("get_verifycode")
            assert login_page[0].query_element(
                element="nophone", mode="wait_for_visible"
            )

        if number == "3":
            login_page[0].bt_click("get_verifycode")
            assert login_page[0].query_element(
                element="success", mode="wait_for_visible"
            )
            assert login_page[0].query_element(element="timer", mode="wait_for_visible")
            login_page[2].wait_for_timeout(60000)
            assert login_page[0].query_element(
                element="resend", mode="wait_for_visible"
            )
            login_page[0].bt_click("get_verifycode")
            assert login_page[0].query_element(
                element="success", mode="wait_for_visible"
            )

    @pytest.mark.parametrize(
        "verifycode,number",
        [
            (rdm(6, False, True, True, True), "1"),
            (rdm(randint(0, 5), True, False, False, False), "2"),
            (rdm(7, True, False, False, False), "3"),
            (rdm(6, True, False, False, False), "4"),
        ],
        ids=["输入非数字", "输入不足6位数", "输入7位数", "输入6位数"],
    )
    def test_verifycode_input(self, login_page, verifycode, number):
        """测试验证码输入框"""

        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")
        # 输入11位手机号
        login_page[0].value_input({"phone_number": rdm(11, True, False, False, False)})
        # 输入验证码
        login_page[0].value_input({"verifycode": verifycode})
        # 断言
        if number == "1":
            assert login_page[0].get_value("verifycode") == ""
        if number == "2":
            assert login_page[0].get_value("verifycode") == verifycode
            assert not login_page[0].query_element(element="login", mode="enable")
        if number == "3":
            assert login_page[0].get_value("verifycode") == verifycode[:6]
        if number == "4":
            assert login_page[0].get_value("verifycode") == verifycode

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
        #保存登录页
        org_page = login_page[2]
        with login_page[1].expect_page() as new_pages:
            login_page[0].a_goto(int(number))
        if new_pages:
            assert target_url in new_pages.value.url
        else:
            assert False, "new_pages 为空"
        #返回登录页
        org_page.bring_to_front()

    def test_disagree_login(self,login_page):
        """测试未同意协议登录"""

        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")

        #输入手机号和验证码
        login_page[0].value_input({"phone_number": "17102108412","verifycode": "000000"})
        #勾选同意协议
        login_page[0].bt_click("agreement")
        assert login_page[0].query_element(
            "agreement_attribute",
            mode="get_attribute",
            attribute="aria-checked"
        ) == "true"

        #取消勾选
        login_page[0].bt_click("agreement")
        assert login_page[0].query_element(
            "agreement_attribute",
            mode="get_attribute",
            attribute="aria-checked"
        ) == "false"

        #点击登录
        login_page[0].bt_click("login")
        assert login_page[0].query_element("dialog",mode = "wait_for_visible")
        #关闭对话框
        login_page[0].bt_click("dialog_close")
        assert not login_page[0].query_element("dialog", mode="wait_for_visible")
        #点击登录
        login_page[0].bt_click("login")
        #点击不同意
        login_page[0].bt_click("dialog_disagree")
        assert not login_page[0].query_element("dialog", mode="wait_for_visible")
        #点击登录
        login_page[0].bt_click("login")

        #保存登录页
        org_page = login_page[2]
        elements = {
            "dialog_a0":"https://dev-learn.u-shannon.com/userAgreement.html",
            "dialog_a1":"https://dev-learn.u-shannon.com/privacyPolicy.html",
        }
        for element,target_url in elements.items():
            with login_page[1].expect_page() as new_pages:
                login_page[0].bt_click(element)
            if new_pages:
                assert target_url in new_pages.value.url
            else:
                assert False, "new_pages 为空"
            #返回登录页
            org_page.bring_to_front()


        #点击同意
        login_page[0].bt_click("dialog_agree")

        try:
            login_page[2].wait_for_url(
                "https://dev-learn.u-shannon.com/", timeout=10000
            )
            assert True
        except TimeoutError:
            assert False, "超时未跳转到指定url"

            # 由于登录后进入了主页，影响其他用例执行，需要返回登录页
        finally:

            # 清除 LocalStorage ，其中包含了token
            login_page[2].evaluate("localStorage.clear();")
            login_page[2].goto(URLDve.OJ_front)































