import iio
import numpy as np
import time

tx_dev = iio.Context('usb:' + '0456' + ':' + 'b673')
rx_dev = iio.Context('usb:' + '0456' + ':' + 'b673')
# tx_buff = tx_dev.find_device('ad9364-phy').find_channel('voltage0')
tx_buff = tx_dev.find_device("cf-ad9361-dds-core-lpc").find_channel("voltage0")
rx_buff = rx_dev.find_device("cf-ad9361-lpc").find_channel("voltage0")

tx_buff.attrs['frequency'].value = str(2.4e9)
tx_buff.attrs['scale'].value = str(1)
tx_buff.attrs['sampling_frequency'].value = str(10e6)

rx_buff.attrs['frequency'].value = str(2.4e9)
rx_buff.attrs['scale'].value = str(1)
rx_buff.attrs['sampling_frequency'].value = str(10e6)

# Convert the message to binary
msg = "Hello World"
msg_bin = ''.join(format(ord(c), '08b') for c in msg)

# Generate the spreading sequence
spreading_seq = np.random.randint(0, 2, size=64)
spreading_seq[spreading_seq == 0] = -1

# Modulate the data using DSSS
dsss_seq = np.zeros(len(msg_bin) * len(spreading_seq))
for i, bit in enumerate(msg_bin):
    dsss_seq[i*len(spreading_seq):(i+1)*len(spreading_seq)] = int(bit) * spreading_seq

# Scale the DSSS sequence to the DAC range
dsss_seq = dsss_seq * 0.7

# Transmit the DSSS sequence
for sample in dsss_seq:
    tx_buff.write([int(sample)])
    time.sleep(0.001)

tx_buff.dispose()
rx_buff.dispose()
tx_dev.dispose()
rx_dev.dispose()
