#用于加载json和csv文件

import json
import csv
import os
from utils.logger import log

def json_loader(*file_name:str):
    #从test_data目录开始，每个层级作用一个变量输入，根据输入顺序拼接任意层级地址
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data',*file_name)
        if not os.path.exists(file_path):
            log.error("数据文件路径错误")
            raise FileNotFoundError("数据文件路径错误")
        with open(file_path,'r',encoding='utf-8') as json_file:
            data = json.load(json_file)
            log.debug("打开数据文件成功")
            return data
    except json.JSONDecodeError as json_error:
        log.error("数据文件json格式错误")
        raise json_error
    except Exception as unknown_error:
        log.error(f"打开数据文件未知错误，错误信息：{unknown_error}")
        raise unknown_error



def csv_loader(*file_name):
    # 从test_data目录开始，每个层级作用一个变量输入，根据输入顺序拼接任意层级地址
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data',*file_name)
        if not os.path.exists(file_path):
            log.error("数据文件路径错误")
            raise FileNotFoundError("数据文件路径错误")
        with open(file_path,'r',encoding='utf-8') as csv_file:
            csv_data = csv.DictReader(csv_file)
            log.debug("打开数据文件成功")
            return [row for row in csv_data]
    except csv.Error as csv_error:
        log.error("数据文件csv解析错误")
        raise csv_error
    except Exception as unknown_error:
        log.error(f"打开数据文件未知错误，错误信息：{unknown_error}")
        raise unknown_error

