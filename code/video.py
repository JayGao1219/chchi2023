import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands.Hands()
        self.prev_landmarks = None

    def start_tracking(self):
        cap = cv2.VideoCapture(0)

        while True:
            success, frame = cap.read()

            if not success:
                print("无法读取摄像头帧")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.mp_hands.process(image)

            num_hands = 0

            if results.multi_hand_landmarks:
                num_hands = len(results.multi_hand_landmarks)

                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                    self.calculate_speed_and_direction(image, hand_landmarks)

            cv2.putText(image, f"Hand Count: {num_hands}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            cv2.imshow("Hand Tracking", image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("退出")
                break

        cap.release()
        cv2.destroyAllWindows()

    def calculate_speed_and_direction(self, image, hand_landmarks):
        if self.prev_landmarks is not None:
            curr_landmarks = hand_landmarks.landmark

            displacements = []
            for prev_pt, curr_pt in zip(self.prev_landmarks, curr_landmarks):
                dx = curr_pt.x - prev_pt.x
                dy = curr_pt.y - prev_pt.y
                displacements.append((dx, dy))

            avg_dx = sum(dx for dx, _ in displacements) / len(displacements)
            avg_dy = sum(dy for _, dy in displacements) / len(displacements)

            speed = (avg_dx ** 2 + avg_dy ** 2) ** 0.5

            angle = math.atan2(avg_dy, avg_dx)
            angle_deg = math.degrees(angle)
            
            direction_text=""
            if abs(dx)>0.03 and abs(dx)>abs(dy):
                if avg_dx < 0:
                    direction_text += "Left"
                elif avg_dx > 0:
                    direction_text += "Right"

            if abs(dy)>0.03 and abs(dy)>abs(dx):
                if avg_dy < 0:
                    direction_text += "Up"
                elif avg_dy > 0:
                    direction_text += "Down"

            cv2.putText(image, f"Speed: {speed:.2f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"dx,dy: {dx:.2f},{dy:.2f}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Direction: {direction_text}", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        self.prev_landmarks = hand_landmarks.landmark

# Instantiate the HandTracker class and call the start_tracking() method to begin tracking
hand_tracker = HandTracker()
hand_tracker.start_tracking()
