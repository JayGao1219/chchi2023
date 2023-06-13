import pprint
import time
import numpy as np

from ifxAvian import Avian
from internal.fft_spectrum import *

def radar_plot(starttime, tot_time, file_root):

    # 参考之前代码中的配置
    config = Avian.DeviceConfig(
        sample_rate_Hz = 1_000_000,       # 1MHZ
        rx_mask = 7,                      # activate RX1 RX2 and RX3
        tx_mask = 1,                      # activate TX1
        if_gain_dB = 33,                  # gain of 33dB
        tx_power_level = 31,              # TX power level of 31
        start_frequency_Hz = 58e9,        # 58.9GHz 
        end_frequency_Hz = 63e9,        # 63.9GHz
        num_chirps_per_frame = 32,       # 32 chirps per frame
        num_samples_per_chirp = 64,       # 64 samples per chirp
        chirp_repetition_time_s = 0.0005, # 0.5ms
        frame_repetition_time_s = 0.0156,   # 75.476ms, frame_Rate = 13.24Hz
    )

    rdframes_data = []
    rdframes_timestamps = []
    with Avian.Device() as device:
        device.set_config(config)
        # get metrics and print them
        metrics = device.metrics_from_config(config)
        pprint.pprint(metrics)

        while True:
            try:
                # frame has dimension num_rx_antennas x num_samples_per_chirp x num_chirps_per_frame
                frame = device.get_next_frame()
                rdframes_data.append(frame)
                rdframes_timestamps.append(time.time()-starttime)
                if time.time()-starttime > tot_time:
                    print("radar time up")
                    break

            except:
                print("ERROR")
                break

    print("save radar and time data")
    np.save(file_root+'radar_frames.npy',np.array(rdframes_data))
    np.save(file_root+'rdframe_timestamp.npy',np.array(rdframes_timestamps))
        
    with open("%sconfig.txt"%(file_root), "w") as f:
        f.write("%s\n%s\n"%(str(config),str(metrics)))
        f.write("tot_time,runtime\n")
        f.write("%d,%d\n"%(tot_time,time.time()-starttime))