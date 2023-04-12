import numpy as np
import matplotlib.pyplot as plt
import uav_frame_info as uavi
import uav_signal as uavs

np.random.seed(42)  # Setting the seed for reproducibility

# Transmission Characteristics
Fs = 900e9
fc = 100
fp = 4
bit_t = 0.1

# generate a message with contents of uav_frame_info.py
frame1 = uavi.UAVFrame(20, 2, 1, 1, 1, 1, 5, 5, -5, -12, 0, -1)
m1 = frame1.get_message()

# generate a seccond message to be sent on the same channel with a
# different PN code
frame2 = uavi.UAVFrame(10, 2, 2, 5, 6, 1, -2, -2, 0, 1, 0, 0)
m2 = frame2.get_message()

# PN code gen to multiply with message
pn_code1 = np.random.randint(0, 2, size=len(m1)*fp)
pn_code2 = np.random.randint(0, 2, size=len(m2)*fp)


# now create a UAVSignal object for each message
signal1 = uavs.UAVSignal(m1, pn_code1, Fs, fc, fp, bit_t)
signal2 = uavs.UAVSignal(m2, pn_code2, Fs, fc, fp, bit_t)

# get the modulated signal 
modulated_signal1 = signal1.modulate()
modulated_signal2 = signal2.modulate()
signal1.demodulate()
signal2.demodulate()
signal1.demodulate_wrong()
signal2.demodulate_wrong()
signal1.plot()
signal2.plot()
plt.show()
# # DSSS encoding
# DSSS = message1 * pn_code1
# DSSS2 = message2 * pn_code2

# # Modulate the two DSSS signals

# t = np.arange(0, (bit_t-1/Fs), 1/1000)
# s0 = np.sin(2 * np.pi * fc * t)
# s1 = -1 * np.sin(2 * np.pi * fc * t)
# carrier = np.array([])
# BPSK = np.array([])


# for i in range(len(DSSS)):
#     if DSSS[i] == 1:
#         BPSK = np.concatenate((BPSK, s1))
#     elif DSSS[i] == -1:
#         BPSK = np.concatenate((BPSK, s0))
    
    
#     carrier = np.concatenate((carrier, s1))



# # Demodulation
# rx = np.array([])
# for i in range(len(pn_code1)):
#     if pn_code1[i] == 1:
#         rx = np.concatenate((rx, BPSK[(i*len(t)):((i+1)*len(t))]))
#     else:
#         rx = np.concatenate((rx, -1 * BPSK[(i*len(t)):((i+1)*len(t))]))

# demod = rx * carrier
# result = np.array([])

# for i in range(len(m1)):
#     x = len(t) * fp
#     cx = np.sum(carrier[(i*x):(i+1)*x] * demod[(i*x):(i+1)*x])
#     if cx > 0:
#         result = np.concatenate((result, [1]))
#     else:
#         result = np.concatenate((result, [-1]))

# # Create a PN code which is wrong
# pn_code_wrong = np.random.randint(0, 2, size=len(m)*fp)
# pn_code_wrong[pn_code_wrong == 0] = -1 

# result_wrong = np.array([])
# rx2 = np.array([])

# for i in range(len(pn_code1)):
#     if pn_code_wrong[i] == 1:
#         rx2 = np.concatenate((rx2, BPSK[(i*len(t)):((i+1)*len(t))]))
#     else:
#         rx2 = np.concatenate((rx2, -1 * BPSK[(i*len(t)):((i+1)*len(t))]))

# # new demodulation
# demod2 = rx2 * carrier

# for i in range(len(m)):
#     x = len(t) * fp
#     cx = np.sum(carrier[(i*x):(i+1)*x] * demod2[(i*x):(i+1)*x])
#     if cx > 0:
#         result_wrong = np.concatenate((result_wrong, [1]))
#     else:
#         result_wrong = np.concatenate((result_wrong, [-1]))

# # now convert result from binary to decimal
# # result = np.array([int(''.join(map(str, result[i:i+8])), 2) for i in range(0, len(result), 8)])
# # result_wrong = np.array([int(''.join(map(str, result_wrong[i:i+8])), 2) for i in range(0, len(result_wrong), 8)])

# # Plotting results
# plt.figure(figsize=(8, 6))
# plt.subplot(3, 1, 1)
# plt.plot(range(len(m)), m, '-o', label='Original message')
# plt.xlabel('Bit index')
# plt.ylabel('Bit value')
# plt.title('DSSS modulation and demodulation')
# plt.legend()
# plt.subplot(3, 1, 2)
# plt.plot(range(len(result)), result, '-o', label='Demodulated message')
# plt.xlabel('Bit index')
# plt.ylabel('Bit value')
# plt.legend()
# plt.subplot(3, 1, 3)
# plt.plot(range(len(result_wrong)), result_wrong, '-o', label='Demodulated message with wrong PN code')
# plt.xlabel('Bit index')
# plt.ylabel('Bit value')
# plt.legend()

# # Print the frames
# print("Transmitted frame: ")
# frame1.print_tx_frame()
# print("\n\nReceived frame: ")
# frame1.print_rx_frame(result)
# print("\n\nReceived frame with wrong PN code: ")
# frame1.print_rx_frame(result_wrong)

# plt.show()



