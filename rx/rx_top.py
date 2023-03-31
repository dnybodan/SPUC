import iio
import time

tx_dev = iio.Context('ip:192.168.2.1')
rx_dev = iio.Context('ip:192.168.2.2')

tx_buff = tx_dev.find_device("cf-ad9361-dds-core-lpc").find_channel("sin")
rx_buff = rx_dev.find_device("cf-ad9361-lpc").find_channel("voltage0")

tx_buff.attrs['frequency'].value = str(2e6)
tx_buff.attrs['scale'].value = str(1)
tx_buff.attrs['sampling_frequency'].value = str(10e6)

rx_data = []

for i in range(1024):
    rx_data.append(int.from_bytes(rx_buff.read(2), byteorder='little', signed=True))

rx_buff.dispose()
tx_buff.dispose()
rx_dev.dispose()
tx_dev.dispose()

print(rx_data)
