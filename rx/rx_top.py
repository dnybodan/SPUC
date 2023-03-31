import iio
import numpy as np

tx_dev = iio.Context('ip:192.168.2.1')
rx_dev = iio.Context('ip:192.168.2.2')

tx_buff = tx_dev.find_device("cf-ad9361-dds-core-lpc").find_channel("voltage0")
rx_buff = rx_dev.find_device("cf-ad9361-lpc").find_channel("voltage0")

tx_buff.attrs['frequency'].value = str(2.4e9)
tx_buff.attrs['scale'].value = str(1)
tx_buff.attrs['sampling_frequency'].value = str(10e6)

rx_buff.attrs['frequency'].value = str(2.4e9)
rx_buff.attrs['scale'].value = str(1)
rx_buff.attrs['sampling_frequency'].value = str(10e6)

# Set the spreading sequence
spreading_seq = np.array([-1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1,
                          -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1,
                          1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1,
                          -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1,
                          -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1,
                          1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1])

# Decode the DSSS signal
rx_data = []
while True:
    samples = rx_buff.read(1024)
    if len(samples) == 0:
        break
    for sample in samples:
        rx_data.append(sample)

msg_dsss = ''
for i in range(0, len(rx_data), len(spreading_seq)):
    symbol = rx_data[i:i+len(spreading_seq)]
    if np.all(symbol == spreading_seq):
        msg_dsss += '1'
    elif np.all(symbol == -spreading_seq):
        msg_dsss += '0'

# Convert the DSSS signal back to text
msg = ''
for i in range(0, len(msg_dsss), 8):
    byte = msg_dsss[i:i+8]
    msg += chr(int(byte, 2))

print(msg)

rx_buff.dispose()
tx_dev.dispose()
rx_dev.dispose()
