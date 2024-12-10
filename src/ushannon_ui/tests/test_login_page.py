import pytest

from utils.logger import log


@pytest.mark.usefixtures("init_page")
class TestLogin:

    def test_login(self, login_page):
        """测试登录"""
        login_page[0].username_input(content="admin")
        login_page[0].password_input(content="xz666666")
        login_page[0].agreement_click()
        login_page[0].login_click()

        try:
            login_page[2].wait_for_url(
                "https://dev-learn.u-shannon.com/", timeout=10000
            )
            assert True
        except TimeoutError:
            assert False, "超时未跳转到指定url"


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
             assert target_url in  new_pages.value.url
        else:
            assert False,"new_pages 为空"
        org_page.bring_to_front()
