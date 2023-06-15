# 预处理雷达数据
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import math

class RadarTracker:
    def __init__(self, root):
        self.root = root
        self.radar_frames = np.load(root + 'radar_frames.npy')
        self.radar_timestamps = np.load(root + 'rdframe_timestamp.npy')
        # 读取result.csv文件
        self.result = []
        with open(root + 'result.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.result.append(row)
        self.time_pair = []
    
    def time_align(self):
        # 根据self.result中的数据，提取出pre_timestamp, cur_timestamp
        # 根据pre_timestamp, cur_timestamp, self.radar_timestamps, self.radar_frames，找到对应的雷达帧
        for i in range(1,len(self.result)):
            pre_timestamp = self.result[i][0]
            cur_timestamp = self.result[i][1]
            speed = self.result[i][2]
            direction = self.result[i][3]
            radar_frame_index = 0
            pre_radar_frame_index = 0
            for j in range(len(self.radar_timestamps)):
                # 找到对应的雷达帧,即找到雷达帧的时间戳与视频帧的时间戳最接近的雷达帧
                if abs(self.radar_timestamps[j] - float(pre_timestamp)) < abs(self.radar_timestamps[radar_frame_index] - float(cur_timestamp)):
                    radar_frame_index = j
                if abs(self.radar_timestamps[j] - float(pre_timestamp)) < abs(self.radar_timestamps[pre_radar_frame_index] - float(pre_timestamp)):
                    pre_radar_frame_index = j
            self.time_pair.append([pre_radar_frame_index, radar_frame_index, speed, direction])
        # 保存time_pair到csv文件中
        with open(self.root + 'time_pair.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.time_pair)

def precess_radar():
    file_root = '../data/'
    actions = ['up', 'down', 'left', 'right', 'clockwise', 'anticlockwise']
    for action in actions:
        folder_path = file_root + action + '/'
        # 获取文件夹下文件夹的数目
        num = len(os.listdir(folder_path))
        for i in range(1, num+1):
            cur_path = folder_path + str(i) + '/'
            print(cur_path)
            radar_tracker = RadarTracker(cur_path)
            radar_tracker.time_align()

if __name__ == '__main__':
    precess_radar()