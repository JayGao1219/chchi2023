# Description: This file contains the code for the video annotation
import cv2
import mediapipe as mp
import math
from collections import deque

class HandTracker:
    def __init__(self,video_path,result_path,n_len):
        self.mp_hands = mp.solutions.hands.Hands()
        self.video_path = video_path
        self.landmarks = deque(maxlen=n_len)
        self.result_path = result_path
        self.distance = deque(maxlen=n_len)

    def start_tracking(self):
        # cap = cv2.VideoCapture(0)
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
                self.calculate_speed_and_direction(image)

            cv2.putText(image, f"Hand Count: {num_hands}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            out.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            # out.write(image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("退出")
                break
        
        print(tot)
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def calculate_speed_and_direction(self, image):

        # 计算节点之间的相对距离
        curr_landmarks = self.landmarks[-1].landmark
        distance = 0.0
        for item in [5,9,13,17]:
            cur = ((curr_landmarks[0].x-curr_landmarks[item].x)**2+ (curr_landmarks[0].y-curr_landmarks[item].y)**2 + (curr_landmarks[0].z-curr_landmarks[item].z)**2)**0.5
            distance += cur
        distance /= 4
        self.distance.append(distance)

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
            diff = self.distance[-1]-self.distance[0]

            direction_text=""
            if abs(diff) < 0.03:
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
            else:
                if diff < 0:
                    direction_text += "Forward"
                else:
                    direction_text += "Backward"
            
            if len(direction_text) == 0:
                direction_text = "Stationary"
            
            speed_text = ""
            if speed < 0.01:
                speed_text = "Stationary"
            elif speed < 0.03:
                speed_text = "Medium"
            else:
                speed_text = "Fast"

            cv2.putText(image, f"Speed: {speed:.4f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"dx,dy: {dx:.4f},{dy:.4f}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Direction: {direction_text}", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image,f"wrist xyz: {curr_landmarks[0].x:.3f},{curr_landmarks[0].y:.3f},{curr_landmarks[0].z:.3f}", (10,150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image,f"distance: {self.distance[-1]:.3f}", (10,180),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image,f"diff distance: {self.distance[-1]-self.distance[0]:.4f}", (10,210),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image,f"diff rate: {(self.distance[-1]-self.distance[0])/self.distance[-1]:.4f}", (10,240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image,f"Speed:: {speed_text}", (10,270),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return image


if __name__ == "__main__":
    # 替换为你要处理的视频文件名
    video_file = "../data/test.avi"
    result_path = "../data/result.avi"
    # Instantiate the HandTracker class and call the start_tracking() method to begin tracking
    hand_tracker = HandTracker(video_file,result_path,3)
    hand_tracker.start_tracking()
