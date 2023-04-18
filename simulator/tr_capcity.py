###############################################################################
# File: tr_capcity.py
# Author: Daniel Nybo
# Date: 4/17/2022
# Revision: 1.0
# Description: This file contains the top level script for the simulation of
#              the UAV protocol. This script is used to test the UAV protocol
#              and its various components. This script is meant to be run in
#              the terminal using the command "python tr_capacity.py". This 
#              script will make use of UAVFrame objects and UAVSignal objects,
#              and will test the functionality of the UAV protocol including
#              the modulation and demodulation of rf-signals and the encoding
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import uav_packet as uavp
import uav_signal as uavs


##############################################################################
# add plot for two added signals with noise added together and recovered
##############################################################################
pn_width = 4
Fs = 900e6
fc = 100
windowperiod = .01

# make signal1
frame1 = uavp.UAVPacket(1,2,3,4,5,6,7,8,9,10,11,12)
m1 = frame1.get_message()
pn_code1 = frame1.get_pn_code(mbits=pn_width)
pn_code1[pn_code1==0] = -1
pn_code1 = np.random.randint(0, 2, pn_width)
signal1 = uavs.UAVSignal(m1, pn_code1, Fs, fc, pn_width, windowperiod)

# make a foo signal to add to the modulated signal
fooframe = uavp.UAVPacket(0, 1, 11, 2, 3, 4, 8, 7, -35, -2, 0, -1)
foo = fooframe.get_message()
foocode = fooframe.get_pn_code(mbits=pn_width)
foo = uavs.UAVSignal(foo, foocode, Fs, fc, pn_width, windowperiod)
foosignal = foo.modulate()

# demonstrate CDMA with the foo signal and the original signal
signal1.modulate(snr=0,addsignal=foosignal, plot=True)
signal1.demodulate(plot=True)
frame1.compare(signal1.result, printTable=True)
signal1.set_pn_code(foocode)
signal1.demodulate(plot=True)
frame1.compare(signal1.result, printTable=True)
fooframe.compare(signal1.result, printTable=True)

plt.show()
