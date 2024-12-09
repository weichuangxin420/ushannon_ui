#用于拼接路径的包
import os

#项目绝对路径
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#data/question_pics的绝对路径
pic_data_path = os.path.join(PROJ_DIR, 'data', "question_pics")

#data/video_log的绝对路径
video_log_path = os.path.join(PROJ_DIR, 'data', "video_log")



if __name__ == "__main__":
    print(PROJ_DIR)
    print(pic_data_path)