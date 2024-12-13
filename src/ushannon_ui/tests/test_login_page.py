import time
from random import randint

import pytest

from config.env import URLDve
from src.utils.decorators import base_decorator
from src.utils.random_data_maker import random_data_maker as rdm
from utils.logger import log


class TestLoginPage:

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "phone",
        ["18210881115", "17102108412", "17102108413", "18210881111", "18210881113"],
        ids=["超管登录", "机构管理员登录", "老师登录", "学生登录", "游客登录"],
    )
    def test_login_phone(self, login_page, phone):
        """测试登录"""
        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")

        # 如果未勾选协议，勾选同意协议
        if (
            login_page[0].query_element(
                "agreement_attribute", mode="get_attribute", attribute="aria-checked"
            )
            == "false"
        ):
            login_page[0].bt_click("agreement")

        # 输入手机号和验证码，并点击登录
        login_page[0].value_input({"phone_number": phone, "verifycode": "000000"})
        login_page[0].bt_click("login")

        try:
            login_page[2].wait_for_url("https://dev-learn.u-shannon.com/", timeout=3000)
            assert True
        except TimeoutError:
            assert False, "超时未跳转到指定url"

            # 由于登录后进入了主页，影响其他用例执行，需要返回登录页
        finally:

            # 清除 LocalStorage ，其中包含了token
            login_page[2].evaluate("localStorage.clear();")
            login_page[2].goto(URLDve.OJ_front)

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "values,tid",
        [
            (rdm(11, False, True, True, True), "1"),
            (rdm(randint(0, 10), True, False, False, False), "2"),
            (rdm(12, True, False, False, False), "3"),
            (rdm(11, True, False, False, False), "4"),
        ],
        ids=["输入非数字字符", "输入11以下的数字", "输入12位数字", "输入11位数字"],
    )
    def test_phone_input(self, login_page, values, tid):
        """测试输入框输入"""
        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")
        login_page[0].value_input({"phone_number": values})
        if tid == "1":
            assert login_page[0].get_value("phone_number") == ""
        if tid == "2":
            assert login_page[0].get_value("phone_number") == values
        if tid == "3":
            assert login_page[0].get_value("phone_number") == values[0:11]
        if tid == "4":
            assert login_page[0].get_value("phone_number") == values
        login_page[0].input_clear("phone_number")

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "phone_number,tid",
        [("17102108412", "1"), ("14000200000", "2"), ("17102108412", "3")],
        ids=["无网获取验证码", "手机号未注册", "成功发送,倒计时后重新发送"],
    )
    def test_get_verifycode(self, login_page, phone_number, tid):
        """测试手机号输入框"""

        # 每次执行恢复网络
        login_page[1].set_offline(False)
        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")
        # 输入手机号
        login_page[0].value_input({"phone_number": phone_number})

        # 断言断网吐司
        if tid == "1":
            login_page[1].set_offline(True)
            login_page[0].bt_click("get_verifycode")
            assert login_page[0].query_element(
                element="neterror", mode="wait_for_visible"
            )

        if tid == "2":
            login_page[0].bt_click("get_verifycode")
            assert login_page[0].query_element(
                element="nophone", mode="wait_for_visible"
            )

        if tid == "3":
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

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "verifycode,tid",
        [
            (rdm(6, False, True, True, True), "1"),
            (rdm(randint(0, 5), True, False, False, False), "2"),
            (rdm(7, True, False, False, False), "3"),
            (rdm(6, True, False, False, False), "4"),
        ],
        ids=["输入非数字", "输入不足6位数", "输入7位数", "输入6位数"],
    )
    def test_verifycode_input(self, login_page, verifycode, tid):
        """测试验证码输入框"""

        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")
        # 输入11位手机号
        login_page[0].value_input({"phone_number": rdm(11, True, False, False, False)})
        # 输入验证码
        login_page[0].value_input({"verifycode": verifycode})
        # 断言
        if tid == "1":
            assert login_page[0].get_value("verifycode") == ""
        if tid == "2":
            assert login_page[0].get_value("verifycode") == verifycode
            assert not login_page[0].query_element(element="login", mode="enable")
        if tid == "3":
            assert login_page[0].get_value("verifycode") == verifycode[:6]
        if tid == "4":
            assert login_page[0].get_value("verifycode") == verifycode

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "target_url,tid",
        [
            ("https://dev-learn.u-shannon.com/userAgreement.html", "0"),
            ("https://dev-learn.u-shannon.com/privacyPolicy.html", "1"),
            ("https://beian.miit.gov.cn/", "2"),
            ("https://beian.mps.gov.cn/#/query/webSearch", "3"),
        ],
    )
    def test_goto(self, login_page, target_url, tid):
        """测试跳转"""
        # 保存登录页
        org_page = login_page[2]
        with login_page[1].expect_page() as new_pages:
            login_page[0].a_goto(int(tid))
        if new_pages:
            assert target_url in new_pages.value.url
        else:
            assert False, "new_pages 为空"
        # 返回登录页
        org_page.bring_to_front()

    @base_decorator(log_level="info")
    def test_disagree_login(self, login_page):
        """测试未同意协议登录"""

        # 切换下手机号登录
        login_page[0].bt_click("phone_login")

        # 输入手机号和验证码
        login_page[0].value_input(
            {"phone_number": "17102108412", "verifycode": "000001"}
        )
        # 勾选同意协议
        login_page[0].bt_click("agreement")
        assert (
            login_page[0].query_element(
                "agreement_attribute", mode="get_attribute", attribute="aria-checked"
            )
            == "true"
        )

        # 取消勾选
        login_page[0].bt_click("agreement")
        assert (
            login_page[0].query_element(
                "agreement_attribute", mode="get_attribute", attribute="aria-checked"
            )
            == "false"
        )

        # 点击登录
        login_page[0].bt_click("login")
        assert login_page[0].query_element("dialog", mode="wait_for_visible")
        # 关闭对话框
        login_page[0].bt_click("dialog_close")
        assert not login_page[0].query_element("dialog", mode="wait_for_visible")
        # 点击登录
        login_page[0].bt_click("login")
        # 点击不同意
        login_page[0].bt_click("dialog_disagree")
        assert not login_page[0].query_element("dialog", mode="wait_for_visible")
        # 点击登录
        login_page[0].bt_click("login")

        # 保存登录页
        org_page = login_page[2]
        elements = {
            "dialog_a0": "https://dev-learn.u-shannon.com/userAgreement.html",
            "dialog_a1": "https://dev-learn.u-shannon.com/privacyPolicy.html",
        }
        for element, target_url in elements.items():
            with login_page[1].expect_page() as new_pages:
                login_page[0].bt_click(element)
            if new_pages:
                assert target_url in new_pages.value.url
            else:
                assert False, "new_pages 为空"
            # 返回登录页
            org_page.bring_to_front()

        # 点击同意
        login_page[0].bt_click("dialog_agree")

        # 断言验证码错误
        assert login_page[0].query_element("wrong_verifycode", mode="wait_for_visible")

        # 更新为正确的验证码再登录
        login_page[0].input_clear("verifycode")
        login_page[0].value_input({"verifycode": "000000"})
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

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "phone,verifycode,tid",
        [
            (None, "000000", "1"),
            ("14000200000", "000000", "2"),
            ("17102108412", None, "3"),
            ("17102108412", rdm(6), "4"),
            ("17102108412", rdm(6), "5"),
        ],
        ids=["手机号为空", "手机号未注册", "验证码为空", "验证码错误", "未获取验证码"],
    )
    def test_process(self, login_page, phone, verifycode, tid):
        """测试登录流程"""

        # 如果不是手机号登录，切换下手机号登录
        if login_page[0].query_element("phone_login", mode="visible"):
            login_page[0].bt_click("phone_login")

        # 如果未勾选协议，勾选同意协议
        if (
            login_page[0].query_element(
                "agreement_attribute", mode="get_attribute", attribute="aria-checked"
            )
            == "false"
        ):
            login_page[0].bt_click("agreement")

        # 输入手机号,获取并输入验证码
        if phone:
            login_page[0].value_input({"phone_number": phone})
        if verifycode:
            login_page[0].value_input({"verifycode": verifycode})

        # 断言登录无法点击
        if tid == "1" or tid == "3":
            assert not login_page[0].query_element("login", mode="enable")
            login_page[0].input_clear(("phone_number", "verifycode"))
            return True

        # 点击登录
        login_page[0].bt_click("login")

        # 断言
        if tid == "2":
            assert login_page[0].query_element("nophone", mode="wait_for_visible")
        if tid == "4":
            assert login_page[0].query_element(
                "wrong_verifycode", mode="wait_for_visible"
            )
        if tid == "5":
            assert login_page[0].query_element(
                "wrong_verifycode", mode="wait_for_visible"
            )

        # 清空原本的输入
        login_page[0].input_clear(("phone_number", "verifycode"))

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "value,tid",
        [
            (rdm(2), "1"),
            (rdm(2, integer=False, letter=True), "2"),
            (rdm(2, integer=False, punctuation=True), "3"),
            (rdm(2, integer=False, chinese=True), "4"),
            (rdm(8, letter=True, punctuation=True, chinese=True), "5"),
        ],
        ids=["输入纯数字", "输入纯英文", "输入纯符号", "输入纯汉字", "混合输入"],
    )
    def test_username_password(self, login_page, value, tid):
        """测试用户名输入框和密码输入框"""

        # 如果是验证码登录，切换为账号密码登录
        if login_page[0].query_element("username_login", mode="wait_for_visible"):
            login_page[0].bt_click("username_login")

        # 输入用户名
        login_page[0].value_input({"username": value})
        login_page[0].value_input({"password": value})

        # 断言
        if tid == "1" or tid == "2":
            # 断言输入保留
            assert login_page[0].get_value("username") == value
            assert (
                login_page[0].query_element(
                    "password", mode="get_attribute", attribute="value"
                )
                == value
            )
            # 删除字符
            login_page[0].exist("username").press("Delete")
            login_page[0].exist("password").press("Delete")
            # 断言正常删除字符
            assert login_page[0].get_value("username") == value[1:]
            assert (
                login_page[0].query_element(
                    "password", mode="get_attribute", attribute="value"
                )
                == value[1:]
            )

        if tid == "3":
            # 断言输入无效
            assert login_page[0].get_value("username") == ""
            assert (
                login_page[0].query_element(
                    "password", mode="get_attribute", attribute="value"
                )
                == value
            )
            # 断言默认隐藏密码
            assert (
                login_page[0].query_element(
                    "password", mode="get_attribute", attribute="type"
                )
                == "password"
            )
            # 点击隐藏按钮
            login_page[0].bt_click("hide")
            # 断言密码不隐藏
            assert (
                login_page[0].query_element(
                    "password", mode="get_attribute", attribute="type"
                )
                == "text"
            )

        if tid == "4":
            # 断言输入无效
            assert login_page[0].get_value("username") == ""
            assert (
                login_page[0].query_element(
                    "password", mode="get_attribute", attribute="value"
                )
                == ""
            )

        if tid == "5":
            # 断言部分输入无效
            assert len(login_page[0].get_value("username")) <= 8
            assert (
                len(
                    login_page[0].query_element(
                        "password", mode="get_attribute", attribute="value"
                    )
                )
                <= 8
            )

        # 清除输入
        login_page[0].input_clear("username")
        login_page[0].input_clear("password")

    @base_decorator(log_level="info")
    @pytest.mark.parametrize(
        "username,password,tid",
        [
            ("testxiaoxin18", "xizhi666", "1"),
            ("testxiaoxin16", "xizhi666", "2"),
            ("testxiaoxin15", "xizhi666", "3"),
            ("testxiaoxin6", "xizhi666", "4"),
            ("testxiaoxin21", "xizhi666", "5"),
            ("testxiaoxin100", "xizhi666", "6"),
            ("testxiaoxin18", "xizhi667", "7"),
            ("testxiaoxin17", "xizhi666", "8"),
            ("testxiaoxin18", "xizhi666", "9"),
        ],
        ids=[
            "游客登录",
            "学生登录",
            "教师登录",
            "机构管理员登录",
            "超管登录",
            "未注册用户登录",
            "错误密码登录",
            "停用账号登录",
            "断网登录",
        ],
    )
    def test_login_username(self, login_page, username, password, tid):

        # 如果是手机号登录，切换为用户名登录
        if login_page[0].query_element("username_login", mode="wait_for_visible"):
            login_page[0].bt_click("username_login")

        # 如果未勾选协议，勾选协议
        if (
            login_page[0].query_element(
                "agreement_attribute", mode="get_attribute", attribute="aria-checked"
            )
            == "false"
        ):
            login_page[0].bt_click("agreement")

        # 输入用户名和密码
        login_page[0].value_input({"username": username, "password": password})
        # 点击登录
        if tid == "9":
            login_page[1].set_offline(True)
        login_page[0].bt_click("login")

        if tid in ["1", "2", "3", "4", "5"]:
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

        if tid == "6":
            # 断言出现吐司文案
            assert login_page[0].query_element("unsigned", mode="wait_for_visible")
        if tid == "7":
            # 断言出现吐司文案
            assert login_page[0].query_element("wrong_password", mode="wait_for_visible")
        if tid == "8":
            # 断言出现吐司文案
            assert login_page[0].query_element("disable_user", mode="wait_for_visible")
        if tid == "9":
            # 断言断网吐司并恢复网络
            assert login_page[0].query_element("neterror", mode="wait_for_visible")
            login_page[1].set_offline(False)
