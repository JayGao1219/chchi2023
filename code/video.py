#  Description: This file contains the code for the video annotation
import cv2
import mediapipe as mp
import math
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import csv

class HandTracker:
    def __init__(self,root,n_len):
        self.mp_hands = mp.solutions.hands.Hands()
        self.video_path = root + 'out.avi' 
        self.landmarks = deque(maxlen=n_len)
        self.t = deque(maxlen=n_len)
        self.result_path = root + 'result.avi' 
        self.timestamps = np.load(root+'video_timestamps.npy')
        self.annotate = []

    def save_annotation(self, pre_timestamp, cur_timestamp, speed, direction):
        annotation = {
            'pre_timestamp': pre_timestamp,
            'cur_timestamp': cur_timestamp,
            'speed': speed,
            'direction': direction
        }
        self.annotate.append(annotation)

    def start_tracking(self):
        cap = cv2.VideoCapture(self.video_path)
        # 获取原始视频的宽度、高度和帧率
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # 创建新的视频写入对象
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.result_path, fourcc, fps, (width, height))

        tot=0
        while cap.isOpened():
            tot+=1
            success, frame = cap.read()

            if not success:
                print("无法读取视频帧")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.mp_hands.process(image)

            num_hands = 0

            if results.multi_hand_landmarks:
                num_hands = len(results.multi_hand_landmarks)
                if num_hands > 1:
                    print("检测到多只手，只跟踪第一只手")
                self.landmarks.append(results.multi_hand_landmarks[0])
                self.t.append(self.timestamps[tot-1])
                self.calculate_speed_and_direction(image)

            cv2.putText(image, f"Hand Count: {num_hands}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            out.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            # out.write(image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("退出")
                break
        
        print("帧数和时间戳")
        print(tot)
        print(len(self.timestamps))
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        # 将self.annotate保存到csv文件中
        with open(self.result_path[:-4]+'.csv', 'w', newline='') as csvfile:
            fieldnames = ['pre_timestamp', 'cur_timestamp', 'speed', 'direction']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for annotation in self.annotate:
                writer.writerow(annotation)
        
        print("视频处理完成")

    def calculate_speed_and_direction(self, image):

        # 计算节点之间的相对距离
        curr_landmarks = self.landmarks[-1].landmark

        if len(self.landmarks) > 1:
            curr_landmarks = self.landmarks[-1].landmark
            prev_landmarks = self.landmarks[0].landmark

            displacements = []
            tot = 0
            for prev_pt, curr_pt in zip(prev_landmarks, curr_landmarks):
                if tot not in [0,5,9,13,17]:
                    tot+=1
                    continue
                tot+=1
                dx = curr_pt.x - prev_pt.x
                dy = curr_pt.y - prev_pt.y
                displacements.append((dx, dy))

            avg_dx = sum(dx for dx, _ in displacements) / len(displacements)
            avg_dy = sum(dy for _, dy in displacements) / len(displacements)

            speed = (avg_dx ** 2 + avg_dy ** 2) ** 0.5

            direction_text=""
            if abs(dx)>abs(dy) and abs(dx)>0.03:
                if avg_dx < 0:
                    direction_text += "Left"
                elif avg_dx > 0:
                    direction_text += "Right"

            if abs(dy)>abs(dx) and abs(dy)>0.03:
                if avg_dy < 0:
                    direction_text += "Up"
                elif avg_dy > 0:
                    direction_text += "Down"
            
            if len(direction_text) == 0:
                direction_text = "Stationary"
            
            speed_text = ""
            if speed < 0.01:
                speed_text = "Stationary"
            elif speed < 0.03:
                speed_text = "Medium"
            else:
                speed_text = "Fast"
            
            self.save_annotation(self.t[0], self.t[-1], speed_text, direction_text)

            cv2.putText(image, f"Speed: {speed:.4f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"dx,dy: {dx:.4f},{dy:.4f}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Direction: {direction_text}", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image,f"Speed:: {speed_text}", (10,150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)



if __name__ == "__main__":
    file_root = '../data/up/1/'
    # Instantiate the HandTracker class and call the start_tracking() method to begin tracking
    hand_tracker = HandTracker(file_root,3)
    hand_tracker.start_tracking()