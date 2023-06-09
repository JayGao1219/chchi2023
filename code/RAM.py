# ===========================================================================
# Copyright (C) 2022 Infineon Technologies AG
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ===========================================================================

import pprint

from ifxAvian import Avian
from internal.fft_spectrum import *

import time

# -------------------------------------------------
# Main logic
# -------------------------------------------------
def radar_plot(frames, starttime, timestamps, tot_time, file_root):

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

    with Avian.Device() as device:
        device.set_config(config)
        # get metrics and print them
        metrics = device.metrics_from_config(config)
        pprint.pprint(metrics)

        while True:
            try:
                # frame has dimension num_rx_antennas x num_samples_per_chirp x num_chirps_per_frame
                frame = device.get_next_frame()
                frames.append(frame)
                timestamps.append(time.time_ns()-starttime)
                if (time.time_ns()-starttime)/1e9 > tot_time:
                    break
            except:
                break

    with open("%sconfig.txt"%(file_root), "w") as f:
        f.write("%s\n%s\n"%(str(config),str(metrics)))
        f.write("tot_time,runtime\n")
        f.write("%d,%d\n"%(tot_time,time.time_ns()-starttime))