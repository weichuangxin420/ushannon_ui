import pytest
from playwright.sync_api import sync_playwright

from src.config.env import URLDve
from src.utils.logger import log

failed_flag = False


def pytest_runtest_makereport(item, call):
    """
    在每个阶段（setup、call、teardown）结束后触发，用于生成报告。
    如果检测到测试用例失败，则设置全局失败标志。
    """
    global failed_flag
    if call.when == "call" and call.excinfo is not None:  # 如果在测试用例执行阶段失败
        failed_flag = True


def pytest_runtest_setup(item):
    """
    在每个测试用例运行前触发，用于检查是否需要跳过测试。
    如果发现之前有失败的用例，则跳过当前测试。
    """
    global failed_flag
    if failed_flag:  # 如果发现之前的用例失败，跳过后续用例
        pytest.skip(f"跳过：由于测试用例 '{item.name}' 之前有失败用例")


@pytest.fixture(scope="class")
def init_page():
    # 初始化
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.set_default_timeout(10000)
    log.debug("浏览器启动成功")
    page = context.new_page()
    page.goto(URLDve.OJ_front)

    # 返回上下文
    yield context, page

    # 关闭释放服务
    context.close()
    browser.close()
    playwright.stop()
    log.debug("浏览器关闭成功")


@pytest.fixture(scope="function")
def login_page(init_page):
    """登录页"""
    if init_page:
        context = init_page[0]
        page = init_page[1]
        from src.ushannon_ui.pages.login import LoginPage

        login_page = LoginPage(page)
        return login_page, context, page
    else:
        log.error("context为空")
