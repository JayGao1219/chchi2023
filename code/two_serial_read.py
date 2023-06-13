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
    
    start = time.time()
    print(start)
    # Create two processes as follows
    try:
        radar = multiprocessing.Process(target=RAM.radar_plot, args=(start,tot_time,file_root))
        video = multiprocessing.Process(target=CAMERA.get_video,args=(start,tot_time,file_root))
      
        radar.start()
        print('RADAR process successfully started!')
        
        video.start()
        print("Video process successfully started!")        
       
    except:
        print("Error: unable to start thread")
