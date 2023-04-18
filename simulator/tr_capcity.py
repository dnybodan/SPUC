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

# make another foo signal to add to the modulated signal
fooframe2 = uavp.UAVPacket(0, 1, 11, 2, 3, 4, 8, 7, -35, -2, 0, -1)
foo2 = fooframe2.get_message()
foocode2 = fooframe2.get_pn_code(mbits=pn_width)
foo2 = uavs.UAVSignal(foo2, foocode2, Fs, fc, pn_width, windowperiod)
foosignal2 = foo2.modulate()

# add the two foo signals together
foosignal = foosignal + foosignal2

# demonstrate CDMA with the foo signal and the original signal
signal1.modulate(SNR=1000, addsignal=foosignal2, plot=True)
signal1.demodulate(plot=True)
frame1.compare(signal1.result, printTable=True)
signal1.set_pn_code(foocode)
signal1.demodulate(plot=True)
frame1.compare(signal1.result, printTable=True)
fooframe.compare(signal1.result, printTable=True)


############################################################################
# demonstrate CDMA capacity by creating a bunch of signals and adding them
# to the original signal until the original signal is no longer recovered 
# perfectly with no noise added 
############################################################################
NUM_BERS = 50
def createInterferingSignal():
    # create a random frame
    frame = uavp.UAVPacket(np.random.randint(0,128),np.random.randint(0,128),np.random.randint(0,128),\
                        np.random.randint(0,128),np.random.randint(0,128),np.random.randint(0,128),\
                            np.random.randint(0,128),np.random.randint(0,128),np.random.randint(0,128))
    m = frame.get_message()
    pn_code = frame.get_pn_code(mbits=pn_width)
    signal = uavs.UAVSignal(m, pn_code, Fs, fc, pn_width, windowperiod)
    return frame, signal

BERs = []

for i in range(0, NUM_BERS):
    # create a list of interfering signals
    interfering_signals = []
    interfering_frames = []
    for i in range(0, 10):
        frame, signal = createInterferingSignal()
        interfering_signals.append(signal)
        interfering_frames.append(frame)

    num_wrong = 0

    # add the interfering signals to the original signal
    for i in range(0, len(interfering_signals)):
        sig = 0
        for j in range(0, i):
            sig += interfering_signals[j].modulate()
        signal1.modulate(addsignal=sig, plot=False)
        signal1.demodulate()
        if not frame1.compare(signal1.result):
            # num bits recovered incorrectly
            for j in range(0, len(signal1.original_message)):
                if signal1.original_message[j] != signal1.result[j]:
                    num_wrong += 1
    BERs.append(num_wrong/(len(signal1.original_message)*10))
# print("Number of bits recovered incorrectly: ", num_wrong)
# print("BER: ", num_wrong/(len(signal1.original_message)*10))

# make a plot of the BER vs the number of interfering signals
plt.figure()
plt.plot(BERs)
plt.xlabel("Number of Interfering Signals")
plt.ylabel("BER")
plt.title("BER vs Number of Interfering Signals")

plt.show()
