import pytest
from playwright.sync_api import sync_playwright

from src.config.env import URLDve
from src.utils.logger import log


@pytest.fixture(scope="class")
def init_page():
    # 初始化
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    log.debug("浏览器启动成功")
    page = context.new_page()

    # 返回上下文
    yield context, page

    # 关闭释放服务
    context.close()
    browser.close()
    playwright.stop()
    log.debug("浏览器关闭成功")


@pytest.fixture(scope="function")
def login_page(init_page):
    if init_page:
        context = init_page[0]
        page = init_page[1]
        page.goto(URLDve.OJ_front)
        from src.ushannon_ui.pages.login import LoginPage

        login_page = LoginPage(page)
        return login_page, context, page
    else:
        log.error("context为空")
        raise
