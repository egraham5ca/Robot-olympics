import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0

data_out = [0xAA, 0x55, 0xFF]
data_in = spi.xfer2(data_out)

print("Sent:     ", data_out)
print("Received: ", data_in)

spi.close()
