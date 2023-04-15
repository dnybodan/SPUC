import numpy as np
import matplotlib.pyplot as plt
import simulations.uav_packet as uavi
# import adi

np.random.seed(42)  # Setting the seed for reproducibility

# Parameters
Fs = 900e6
fc = 100
fp = 4
bit_t = 0.1

# generate a message with contents of uav_frame_info.py
frame = uavi.UAVPacket(20, 2, 1, 1, 1, 1, 5, 5, -5, -12, 0, -1)
m = frame.get_message()

# Message generation with BPSK
m[m == 0] = -1  # Convert 0 to -1 for BPSK modulation

# do the python equivalent of message =  repmat(m,fp,1);
message = np.tile(m, (fp,1))
# now reshape to 1 vector but on axis 1
message = message.T.reshape(1, message.size)[0]

# PN code gen to multiply with message
pn_code = np.random.randint(0, 2, size=len(m)*fp)
# pn_code = np.array([0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1])

# Convert 0 to -1 for DSSS encoding
pn_code[pn_code == 0] = -1
# DSSS encoding
DSSS = message * pn_code
# Modulate the DSSS signal
t = np.arange(0, (bit_t-1/Fs), 1/1000)
s0 = np.sin(2 * np.pi * fc * t)
s1 = -1 * np.sin(2 * np.pi * fc * t)
carrier = np.array([])
BPSK = np.array([])

for i in range(len(DSSS)):
    if DSSS[i] == 1:
        BPSK = np.concatenate((BPSK, s1))
    elif DSSS[i] == -1:
        BPSK = np.concatenate((BPSK, s0))
    carrier = np.concatenate((carrier, s1))

# Demodulation
rx = np.array([])

for i in range(len(pn_code)):
    if pn_code[i] == 1:
        rx = np.concatenate((rx, BPSK[(i*len(t)):((i+1)*len(t))]))
    else:
        rx = np.concatenate((rx, -1 * BPSK[(i*len(t)):((i+1)*len(t))]))

demod = rx * carrier
result = np.array([])

for i in range(len(m)):
    x = len(t) * fp
    cx = np.sum(carrier[(i*x):(i+1)*x] * demod[(i*x):(i+1)*x])
    if cx > 0:
        result = np.concatenate((result, [1]))
    else:
        result = np.concatenate((result, [-1]))

# Create a PN code which is wrong
pn_code_wrong = np.random.randint(0, 2, size=len(m)*fp)
pn_code_wrong[pn_code_wrong == 0] = -1 

result_wrong = np.array([])
rx2 = np.array([])

for i in range(len(pn_code)):
    if pn_code_wrong[i] == 1:
        rx2 = np.concatenate((rx2, BPSK[(i*len(t)):((i+1)*len(t))]))
    else:
        rx2 = np.concatenate((rx2, -1 * BPSK[(i*len(t)):((i+1)*len(t))]))

# new demodulation
demod2 = rx2 * carrier

for i in range(len(m)):
    x = len(t) * fp
    cx = np.sum(carrier[(i*x):(i+1)*x] * demod2[(i*x):(i+1)*x])
    if cx > 0:
        result_wrong = np.concatenate((result_wrong, [1]))
    else:
        result_wrong = np.concatenate((result_wrong, [-1]))

# now convert result from binary to decimal
# result = np.array([int(''.join(map(str, result[i:i+8])), 2) for i in range(0, len(result), 8)])
# result_wrong = np.array([int(''.join(map(str, result_wrong[i:i+8])), 2) for i in range(0, len(result_wrong), 8)])

# Plotting results
plt.figure(figsize=(8, 6))
plt.subplot(3, 1, 1)
plt.plot(range(len(m)), m, '-o', label='Original message')
plt.xlabel('Bit index')
plt.ylabel('Bit value')
plt.title('DSSS modulation and demodulation')
plt.legend()
plt.subplot(3, 1, 2)
plt.plot(range(len(result)), result, '-o', label='Demodulated message')
plt.xlabel('Bit index')
plt.ylabel('Bit value')
plt.legend()
plt.subplot(3, 1, 3)
plt.plot(range(len(result_wrong)), result_wrong, '-o', label='Demodulated message with wrong PN code')
plt.xlabel('Bit index')
plt.ylabel('Bit value')
plt.legend()

# Print the frames
# print("Transmitted frame: ")
# frame.print_tx_frame()
# print("\n\nReceived frame: ")
# frame.print_rx_frame(result)
# print("\n\nReceived frame with wrong PN code: ")
# frame.print_rx_frame(result_wrong)

plt.show()
