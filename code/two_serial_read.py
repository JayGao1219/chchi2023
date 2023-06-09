#!/usr/bin/python3
import time, multiprocessing
import numpy as np
import os

import RAM, CAMERA

def real_time_data(tot_time,file_root,index):
    # 生成目录
    file_root = file_root + str(index) + '/'
    if not os.path.exists(file_root):
        os.makedirs(file_root)
    # 生成雷达数据路径
    manager = multiprocessing.Manager()
    
    frames = manager.list()
    timestamps_rdframes = manager.list()
    videoframe=manager.list()
    
    start = time.time_ns()
    print(start)
    # Create two processes as follows
    try:
        radar = multiprocessing.Process(target=RAM.radar_plot, args=(frames,start, timestamps_rdframes,tot_time))
        video = multiprocessing.Process(target=CAMERA.get_video,args=(videoframe,start,tot_time,file_root))
      
        radar.start()
        print('RADAR process successfully started!')
        
        video.start()
        print("Video process successfully started!")        
       
    except:
        print("Error: unable to start thread")

    try:
        # Wait for processes to finish
        print("save radar and time data")
        # 视频数据在函数中储存
        np.save(file_root+'radar_frames.npy',np.array(frames))
        np.save(file_root+'rdframe_timestamp.npy',np.array(timestamps_rdframes))
        
    except KeyboardInterrupt:
        exit()

