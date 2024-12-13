from src.utils.decorators import exception_catcher as ec
from src.utils.decorators import logger
from src.utils.logger import log
from playwright._impl._errors import TimeoutError as pw_TimeoutError

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
            self.bt_phone_login = self.page.locator("text = 手机验证码登录")
            #切换账号密码等待按钮
            self.bt_username_login = self.page.get_by_text("账号密码登录",exact=True)
            # 用户协议复选框
            self.cb_agreement = self.page.locator(".semi-checkbox-inner-display")
            #用户协议复选框——用于存在性质的元素
            self.cb_agreement2 = self.page.locator("[type = checkbox]")
            # 跳转网页：1.用户协议；2.隐私政策；3.备案网页1；4.备案网页2
            self.a = self.page.locator("div a")
            # 手机号输入框
            self.input_phone = self.page.locator("#phone_number")
            # 验证码输入框
            self.input_verifycode = self.page.locator("#verification_code")
            # 获取验证码按钮
            self.bt_verifycode = self.page.locator("div>[type =button]")
            # 网络错误吐司
            self.toast_neterror = self.page.get_by_text("网络请求失败")
            # 手机号未注册吐司
            self.toast_nophone = self.page.get_by_text("当前手机号未注册")
            # 成功发送吐司
            self.toast_success_send = self.page.get_by_text("发送成功")
            # 重发送倒计时
            self.timer_resend = self.page.get_by_text("59")
            # 重写发送文案
            self.text_resend = self.page.get_by_text("重新获取")
            #协议对话框
            self.dialog = self.page.locator("#dialog-0")
            #对话框关闭按钮
            self.dialog_close = self.page.locator("span [aria-label =close ]")
            #对话框不同意
            self.dialog_disagree = self.page.get_by_text("不同意")
            #对话框同意
            self.dialog_agree = self.page.get_by_text("同意并登录")
            #对话框链接:1是用户协议，2是隐私政策
            self.dialog_a = self.page.locator("._modal-content-link_i6023_49")
            #验证码错误吐司
            self.toast_wrong_verifycode = self.page.get_by_text("验证码不正确")
            #验证码已失效吐司
            self.toast_verifycode_expired = self.page.get_by_text("验证码已失效")
            #隐藏密码按钮
            self.bt_hide_password = self.page.locator("[role = button]")






            # 将元素分类——元素目录(名字不要重复)
            # 输入框
            self.input_boxes = {
                "username": self.input_username,
                "password": self.input_password,
                "phone_number": self.input_phone,
                "verifycode": self.input_verifycode,
            }
            # 按钮
            self.buttons = {
                "login": self.bt_login,
                "agreement": self.cb_agreement,
                "phone_login": self.bt_phone_login,
                "username_login": self.bt_username_login,
                "get_verifycode": self.bt_verifycode,
                "dialog_close": self.dialog_close,
                "dialog_disagree": self.dialog_disagree,
                "dialog_agree": self.dialog_agree,
                "dialog_a0": self.dialog_a.nth(0),
                "dialog_a1": self.dialog_a.nth(1),
                "hide" : self.bt_hide_password
            }

            self.text = {
                "neterror": self.toast_neterror,
                "nophone": self.toast_nophone,
                "success": self.toast_success_send,
                "timer": self.timer_resend,
                "resend": self.text_resend,
                "wrong_verifycode": self.toast_wrong_verifycode,
                "verifycode_expired": self.toast_verifycode_expired,

            }
            self.others = {
                "agreement_attribute": self.cb_agreement2,
                "dialog" : self.dialog,
            }

        except Exception as e_locator:
            log.error(f"元素定位错误{e_locator}")
            raise e_locator

    def exist(self, element):
        """检查函数是否存在目录"""

        #检查输入是否为空
        if element:
            #搜索目录
            locator = (
                self.input_boxes.get(element)
                or self.buttons.get(element)
                or self.text.get(element)
                or self.others.get(element)
            )
            #检查是否存在目录
            if locator:
                return locator
            else:
                log.error("目录中没有该元素")
                return None
        else:
            log.error("该元素为空")
            return False


    @logger
    @ec
    def query_element(self, element, mode,attribute = None):
        """查询元素的性质"""
        modes = ("visible", "wait_for_visible", "enable","get_attribute")
        if element is None:
            log.error("查询参数为空")
            return False
        if mode not in modes:
            log.error("mode的输入不合法")
            return False

        # 获取对应元素（若存在）是否在目录中
        ui_element = self.exist(element)

        # 根据 mode 参数决定处理逻辑
        if mode == "visible":
            return ui_element.is_visible()
        if mode == "wait_for_visible":
            # 等待元素变为可见状态
            try:
                ui_element.wait_for(state="visible",timeout=1000)
                return True
            except pw_TimeoutError:
                return False
        if mode == "enable":
            return ui_element.is_enabled(timeout=100)
        if mode == "get_attribute":
            if attribute:
                return ui_element.get_attribute(attribute)
            else:
                log.error("未输入需要查询的属性，请检查输入参数")
                return False


    @logger
    @ec
    def value_input(self, box_value: dict):
        """向输入框输入内容"""
        # 检查空参
        if box_value is None:
            log.error("box_value为空，请检查输入")
            return False
        # 遍历参数并输入
        for box, value in box_value.items():
            if self.input_boxes.get(box):
                self.input_boxes[box].fill(value)
            else:
                log.error("没有对应的输入框，请检查参数")
                return False
        return True

    @ec
    @logger
    def get_value(self, box: str):
        """获取输入框中的内容"""

        # 检查空参
        if box is None:
            log.error("参数box为空，请检查输入")
            return False

        if self.input_boxes.get(box):
            return self.input_boxes[box].input_value()
        else:
            log.error("没有对应的输入框，请检查参数")
            return False

    @logger
    @ec
    def bt_click(self, bts: tuple | str):
        """点击按钮"""

        # 检查空参
        if bts is None:
            log.error("bts为空，请检查输入")
            return False

        # 将字符串输入认为是单输入，转换为单元素元组
        if type(bts) is str:
            bts = (bts,)

        # 遍历参数并点击
        for bt in bts:
            if self.buttons.get(bt):
                self.buttons[bt].click()
                #为渲染预留时间
                self.page.wait_for_timeout(100)
            else:
                log.error("没有对应的输入框，请检查参数")
                return False

        return True

    @logger
    @ec
    def a_goto(self, nth):
        """前往网页"""
        return self.a.nth(nth).click()

    @logger
    @ec
    def input_clear(self, boxes: tuple | str):
        """清除输入框"""

        # 检查空参数
        if boxes is None:
            log.error("boxes为空，请检查输入")
            return False
        # 兼容字符串
        if type(boxes) is str:
            boxes = (boxes,)

        for box in boxes:
            if self.input_boxes.get(box):
                try:
                    self.input_boxes[box].clear(timeout=100)
                except pw_TimeoutError:
                    log.debug("输入框无内容删除")
            else:
                log.error("没有对应的输入框，请检查参数")
                return False
