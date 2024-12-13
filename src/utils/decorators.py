# 存放装饰器
from functools import wraps
from time import time

from src.utils.logger import log


def base_decorator(log_level):
    """捕获异常并记录日志的装饰器"""

    # 判断是否直接调用
    if callable(
        log_level
    ):  # 如果直接使用 @base_decorator，则 level 实际上是被装饰的函数
        func = log_level  # 被装饰的函数
        level = "debug"  # 默认日志等级

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time = time()
                log.debug(f"{func.__name__}开始执行")
                result = func(*args, **kwargs)
                end_time = time()
                log.debug(f"{func.__name__}执行成功, 耗时{end_time - start_time:.2f}秒")
                return result
            except Exception as e:
                log.error(f"在执行 '{func.__name__}' 时捕获到异常：{e}", exc_info=True)
                raise

        return wrapper

    # 等级映射
    log_levels = {
        "debug": log.debug,
        "info": log.info,
        "error": log.error,
        "critical": log.critical,
    }

    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 计算执行时间
                start_time = time()

                if log_level in log_levels:
                    log_levels[log_level](f"{func.__name__}开始执行")
                else:
                    log.error("装饰器错误，输入的日志等级无效")
                    raise "装饰器错误，输入的日志等级无效"

                result = func(*args, **kwargs)
                end_time = time()

                log_levels[log_level](
                    f"{func.__name__}执行成功,耗时{start_time-end_time:.2f}s"
                )

                return result
            except Exception as e:
                # 记录错误日志，包含函数名称和异常信息
                log.error(f"在执行 '{func.__name__}' 时捕获到异常：{e}", exc_info=True)
                # 重新抛出异常以便上层调用者处理
                raise e

        return wrapper

    return actual_decorator


if __name__ == "__main__":
    #
    @base_decorator(log_level="info")
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
