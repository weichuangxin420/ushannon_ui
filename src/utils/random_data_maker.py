import random
import string


def random_data_maker(
    length=5, integer=True, letter=False, punctuation=False, chinese=False
):
    """用于生成随机的字母，数字，特殊符合的字符串"""
    char_pool = ""
    if integer:
        char_pool += string.digits
    if letter:
        char_pool += string.ascii_letters
    if punctuation:
        char_pool += string.punctuation

    if chinese:
        char_pool += "".join(
            chr(random.randint(0x4E00, 0x9FFF)) for _ in range(30)
        )
    if char_pool:
        return "".join(random.choice(char_pool) for i in range(length))
    else:
        return None


if __name__ == "__main__":
    print(
        random_data_maker(2,integer=False,chinese=True)
    )
