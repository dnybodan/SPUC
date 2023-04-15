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

# enabl CDMA capacity demo NOTE: this will take a long time to run for a large number
# of interfering values
DEMO_CAPACITY = False
# turn on/off plotting
PLOT = True
# specify number of different interfering values to calculate
NUM_BERS = 30


# Setting the seed for reproducibility
np.random.seed(42)

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
modulated_signal1 = signal1.modulate(plot=True)
modulated_signal2 = signal2.modulate(plot=True)
signal1.demodulate(plot = True)
signal2.demodulate()
signal1.demodulate_wrong()
signal2.demodulate_wrong()
signal1.plot_message()
signal2.plot_message()
frame1.print_tx_frame()
frame1.print_rx_frame(signal1.result)
frame2.print_tx_frame()
frame2.print_rx_frame(signal2.result)

############################################################################
# loop over SNR in db to find the SNR at which the message is recovered
############################################################################
# loop over SNR in db to find the SNR at which the message is recovered
# and plot BER vs SNR for the recovered message

# initialize BER array
BERs = np.array([])
snr = -60
num_wrong = 0

while snr < 10:
    num_wrong = 0
    signal1.modulate(SNR=snr, plot=False)
    signal1.demodulate()
    # if frame1.compare(signal1.result):
    #     signal1.modulate(SNR=snr, plot=True)
    #     signal1.modulate(plot=True)
    #     signal1.demodulate(plot=True)
    #     print("SNR = ", snr)
    #     break
    snr += 1
    for j in range(0, len(signal1.original_message)):
                if signal1.original_message[j] != signal1.result[j]:
                    num_wrong += 1
    BERs = np.append(BERs, num_wrong/len(signal1.original_message))
plt.figure()
plt.semilogy(np.arange(-60, 10), BERs, 'bo-')
plt.xlabel("SNR (dB)")
plt.ylabel("BER")
plt.title("BER vs SNR")

############################################################################
# demonstrate CDMA by adding a second signal to the first signal
############################################################################
# make a foo signal to add to the modulated signal

fooframe = uavp.UAVPacket(0, 1, 11, 2, 3, 4, 8, 7, -35, -2, 0, -1)
foo = fooframe.get_message()
foocode = fooframe.get_pn_code(mbits=pn_width)
foo = uavs.UAVSignal(foo, foocode, Fs, fc, pn_width, windowperiod)
foosignal = foo.modulate()

# demonstrate CDMA with the foo signal and the original signal
signal1.modulate(addsignal=foosignal, plot=False)
signal1.demodulate()
frame1.compare(signal1.result, printTable=True)
signal1.set_pn_code(foocode)
signal1.demodulate()
frame1.compare(signal1.result, printTable=True)
fooframe.compare(signal1.result, printTable=True)

############################################################################
# demonstrate CDMA capacity by creating a bunch of signals and adding them
# to the original signal until the original signal is no longer recovered 
# perfectly with no noise added 
############################################################################
if DEMO_CAPACITY:
    def createInterferingSignal():
        # create a random frame
        
        frame = uavp.UAVPacket(np.random.randint(0,128),np.random.randint(0,128),np.random.randint(0,128),\
                            np.random.randint(0,128),np.random.randint(0,128),np.random.randint(0,128),\
                                np.random.randint(0,128),np.random.randint(0,128),np.random.randint(0,128))
        m = frame.get_message()
        pn_code = frame.get_pn_code(mbits=pn_width)
        pn_code = np.random.randint(0, 2, pn_width)
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

##############################################################################

# master plot signal
if(PLOT):
    plt.show()
