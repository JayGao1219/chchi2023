import os
import time

from two_serial_read import real_time_data

def collect_data():
    tot_time = int(input("请输入收集数据的时长（秒）："))
    # 用户选择手势
    gestures = {
        1: "up",
        2: "down",
        3: "left",
        4: "right",
        5: "clockwise",
        6: "anticlockwise"
    }

    print("请选择要收集的手势：")
    for key, value in gestures.items():
        print(f"{key}. {value}")

    gesture_index = int(input("请输入手势编号："))
    gesture_name = gestures[gesture_index]
    print(f"您选择的手势为：{gesture_name}")
    time.sleep(1.5)

    print("开始收集数据，请做好准备！")
    data_directory = "../data/"  # 给定的文件根目录

    # 创建新的文件夹名称
    new_folder_path = os.path.join(data_directory, gesture_name) + "/"
    print("新的文件夹路径为：", new_folder_path)

    # 获取已有的文件夹个数
    num_folders = len(os.listdir(new_folder_path))
    real_time_data(tot_time, new_folder_path, num_folders + 1)

# 调用 collect_data() 函数开始收集数据

if __name__ == '__main__':
    collect_data()
