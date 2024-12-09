import pytest
from playwright.sync_api import sync_playwright

from src.config.env import URLDve
from src.utils.logger import log


@pytest.fixture(scope="function", autouse=True)
def page():
    # 初始化
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    log.debug("浏览器启动成功")
    page = context.new_page()
    page.goto(URLDve.OJ_backend)

    # 返回上下文
    yield page

    # 关闭释放服务
    page.wait_for_timeout(3000)
    context.close()
    browser.close()
    playwright.stop()
    log.debug("浏览器关闭成功")
