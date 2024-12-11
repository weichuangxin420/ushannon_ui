# 存放装饰器


from functools import wraps

from src.utils.logger import log


def exception_catcher(func):
    """捕获异常并记录日志的装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 记录错误日志，包含函数名称和异常信息
            log.error(f"在执行 '{func.__name__}' 时捕获到异常：{e}", exc_info=True)
            # 重新抛出异常以便上层调用者处理
            raise e
    return wrapper


def logger(func):
    """记录日志的装饰器"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        log.debug(f"{func.__name__}执行成功")
        return result

    return wrapper


if __name__ == "__main__":
    #
    @logger
    # @UI_exception_catcher
    def tsum(a, b):
        return a + b

    tsum(1, 2)
    #
    # @http_exception_catcher
    # def t_http():
    #     respond = requests.get("https://baidu.com")
    #     return respond
    # print(t_http())
