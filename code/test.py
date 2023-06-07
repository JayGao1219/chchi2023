import cv2
import mediapipe as mp

# 初始化 MediaPipe 手部组件
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    # 如果摄像头读取失败，跳过当前帧
    if not ret:
        continue

    # 将图像转为 RGB 格式
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 将图像送入 MediaPipe 进行手部关键点检测
    result = hands.process(image)

    # 将图像转回 BGR 格式并绘制手部关键点
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 显示图像
    cv2.imshow("Hand Keypoints", image)

    # 如果按下 'q' 键，退出循环
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Exit")
        break


# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()