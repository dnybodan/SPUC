###############################################################################
# File: tr_top.py
# Author: Daniel Nybo
# Date: 4/14/2022
# Revision: 2.0
# Description: This file contains the top level script for the simulation of
#              the UAV protocol. This script is used to test the UAV protocol
#              and its various components. This script is meant to be run in
#              the terminal using the command "python tr_top.py" given that 
#              the user is in the correct directory and has the uav_frame.py
#              and uav_signal.py files in the same directory. This script
#              will make use of UAVFrame objects and UAVSignal objects, and
#              will test the functionality of the UAV protocol including the
#              modulation and demodulation of rf-signals and the encoding 
#              and decoding of the UAVFrame objects. CDMA Code Division
#              Multiple Access is modeled as well as the effects of channel
#              noise on the demodulation of the signal. This script is meant
#              to be used as a testbed for the UAV protocol and its various
#              components.
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import uav_packet as uavp
import uav_signal as uavs

np.random.seed(42)  # Setting the seed for reproducibility



# generate a message with contents of uav_frame_info.py
frame1 = uavp.UAVPacket(20, 2, 1, 1, 1, 1, 5, 5, -5, -12, 0, -1)
m1 = frame1.get_message()

# generate a seccond message to be sent on the same channel with a
# different PN code
frame2 = uavp.TextPacket(10, 2, 3, 5, 6, 1, -2, -2, 0, 1, 0, 0, "In ECEN 526, we learn about Wi-Fi and its tricks,\
 Hoping to make connections as smooth as butter sticks.")
m2 = frame2.get_message()

# Transmission Characteristics
Fs = 900e6
fc = 100
pn_width = 4
windowperiod = .01

# PN code gen to multiply with message
pn_code1 = np.random.randint(0, 2, pn_width)
pn_code2 = np.random.randint(0, 2, pn_width)

# now create a UAVSignal object for each message
signal1 = uavs.UAVSignal(m1, pn_code1, Fs, fc, pn_width, windowperiod)
signal2 = uavs.UAVSignal(m2, pn_code2, Fs, fc, pn_width, windowperiod)

# get the modulated signal 
# modulated_signal1 = signal1.modulate(SNR=-8,plot=True)
# modulated_signal2 = signal2.modulate()
# signal1.demodulate(plot = True)
# signal2.demodulate()
# signal1.demodulate_wrong()
# signal2.demodulate_wrong()
# signal1.plot_message()
# signal2.plot_message()
# frame1.print_tx_frame()
# frame1.print_rx_frame(signal1.result)
# frame2.print_tx_frame()
# frame2.print_rx_frame(signal2.result)

# make a foo signal to add to the modulated signal
fooframe = uavp.UAVPacket(0, 1, 11, 2, 3, 4, 8, 7, -35, -2, 0, -1)
foo = fooframe.get_message()
foocode = fooframe.get_pn_code(mbits=pn_width)
foo = uavs.UAVSignal(foo, foocode, Fs, fc, pn_width, windowperiod)
foosignal = foo.modulate()

# loop over SNR in db to find the SNR at which the message is recovered
snr = -20
while snr < 10:
    signal1.modulate(SNR=snr, addsignal=foosignal, plot=False)
    signal1.demodulate()
    # frame1.compare(signal1.result)
    if frame1.compare(signal1.result):
        print("SNR = ", snr)
        break
    snr += 1

signal1.demodulate()
frame1.compare(signal1.result, printTable=True)
signal1.set_pn_code(foocode)
signal1.demodulate()
frame1.compare(signal1.result, printTable=True)

plt.show()