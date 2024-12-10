# 用于输出日志

import logging
import os
import time

import colorlog

from src.config.env import Path

# 日志颜色配置
log_colors_config = {
    "DEBUG": "white",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

# 创建日志记录器
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# 获取当前日期
daytime = time.strftime("%Y-%m-%d", time.localtime())

# 设置日志文件路径
path = Path.log_path
if not os.path.exists(path):
    os.makedirs(path)

filename = os.path.join(path, f"log_{daytime}.log")

# 创建控制台处理器并设置级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建文件处理器并设置级别
file_handler = logging.FileHandler(filename=filename, mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 创建格式化器
console_formatter = colorlog.ColoredFormatter(
    fmt="\n%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors=log_colors_config,
)
file_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 为处理器设置格式化器
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# 添加处理器到日志记录器
if not log.handlers:
    log.addHandler(console_handler)
    log.addHandler(file_handler)

# 测试代码
if __name__ == "__main__":
    log.debug("这是调试信息")
    log.info("这是一般信息")
    log.warning("这是警告信息")
    log.error("这是错误信息")
    log.critical("这是严重错误信息")
