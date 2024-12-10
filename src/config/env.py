# 存放环境变量
import os


class Path:
    # 源代码路径
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 日志路径
    log_path = os.path.join(base_path, "data", "logs")


class URLDve:

    LLM = "https://dev-backend.xizi-ai.com"
    OJ_backend = "https://dev-admin.u-shannon.com/"
    OJ_front = "https://dev-learn.u-shannon.com/login"


class LLM:
    access_token = None
    refresh_token = None


class Token:
    token_11_9 = "3b960aa8-754e-4927-b9e9-7aed65c2cf73"


class Unclear:
    user_id = []


if __name__ == "__main__":
    path = Path()
