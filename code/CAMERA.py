import cv2
import time
import numpy as np

def get_video(starttime,tot_time,file_root):
    cap = cv2.VideoCapture(0)

    # 获取默认的宽度和高度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))//2
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))//2

    ret = cap.set(3, width)
    ret = cap.set(4, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(file_root+'out.avi', fourcc, 20.0, (width, height))
    print('video init finish')
    timestamps = []
    while cap.isOpened():
        timestamps.append(time.time()-starttime)
        ret, frame = cap.read()
        if ret is True:
            frame = cv2.resize(frame, (width, height))
            out.write(frame)
            # cv2.imshow('frame', frame)
        else:
            break
        if time.time()-starttime > tot_time:
            print("time up")
            break
 
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    print('video finish')
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    timestamps = np.array(timestamps)
    np.save(file_root+'video_timestamps.npy', timestamps)

if __name__ == '__main__':
    start_time = time.time()
    # 收集数据，上下左右前后
    get_video(start_time,15,'../data/')

