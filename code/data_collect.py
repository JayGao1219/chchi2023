import os

from two_serial_read import real_time_data

def collect_data():
    tot_time = int(input("请输入收集数据的时长（秒）："))
    file_root = "../data/"  # 给定的文件根目录
    index = len(os.listdir(file_root))  # 统计文件夹的数目

    real_time_data(tot_time, file_root, index)

# 调用 collect_data() 函数开始收集数据

if __name__ == '__main__':
    collect_data()
