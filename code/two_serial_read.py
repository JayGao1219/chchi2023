#!/usr/bin/python3

import serial, time, sys, threading, multiprocessing
import IMU, RAM, CAMERA

import pprint
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import savemat
import pprint

if __name__ == "__main__":
    print("in")
    opt = IMU.parse_opt()
    manager = multiprocessing.Manager()
    
    imudata = manager.list()
    frames = manager.list()
    timestamps_rdframes = manager.list()
    videoframe=manager.list()
    
    start = time.time_ns()
    print(start)
    # Create two processes as follows
    try:
        radar = multiprocessing.Process(target=RAM.radar_plot, args=(frames,start, timestamps_rdframes))
        imu = multiprocessing.Process(target=IMU.receive_data, args=(opt, imudata, start))
        video = multiprocessing.Process(target=CAMERA.get_video,args=(videoframe,start))
      
        radar.start()
        print('RADAR process successfully started!')
        
        imu.start()
        print('IMU process successfully started!')

        video.start()
        print("Video process successfully started!")        
       
        # radar.join()
        # imu.join()
       
    except:
        print("Error: unable to start thread")

    try:
        # while True:      
        #     pass
        time.sleep(10)
        print(len(imudata), len(frames))
        print("imu,radar data saved!")
        mdict = {"imu_data": np.array(imudata), "radar_frames":np.array(frames), "rdframe_timestamp":np.array(timestamps_rdframes)}
        # mdict = {"imu_data": list(imudata), "radar_frames":list(frames)}
        savemat("test1.mat", mdict)
        
    except KeyboardInterrupt:
        exit()