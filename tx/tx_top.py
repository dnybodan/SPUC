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

# Encode the message using DSSS
msg = 'Hello World'
msg_bin = ''.join(format(ord(c), '08b') for c in msg)
msg_dsss = ''
for i in range(len(msg_bin)):
    if msg_bin[i] == '1':
        msg_dsss += np.array2string(spreading_seq, separator='')[1:-1]
    else:
        msg_dsss += np.array2string(-spreading_seq, separator='')[1:-1]

# Modulate the DSSS signal
tx_data = []
for i in range(0, len(msg_dsss), len(spreading_seq)):
    symbol = msg_dsss[i:i+len(spreading_seq)]
    tx_data.extend(symbol)

# Write the modulated signal to the TX buffer
for sample in tx_data:
    tx_buff.write([int(sample)])

rx_buff.dispose()
tx_dev.dispose()
rx_dev.dispose()
