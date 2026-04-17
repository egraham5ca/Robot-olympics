#!/usr/bin/python3
# Basic LED test – built-in robot LEDs (SPI)

import time
from spi_ledpixel import Freenove_SPI_LedPixel

class Led:
    def __init__(self):
        # 8 built-in LEDs on Robot Olympics car
        self.strip = Freenove_SPI_LedPixel(
            count=8,
            bright=255,
            sequence='GRB'
        )

    def on(self):
        # Turn all LEDs ON (white)
        self.strip.set_all_led_color(255, 255, 255)

    def off(self):
        # Turn all LEDs OFF
        self.strip.set_all_led_color(0, 0, 0)

    def close(self):
        self.off()
        self.strip.led_close()

# ----------------------------
# Simple standalone test
# ----------------------------
if __name__ == '__main__':
    print("LED test starting...")
    led = Led()
    try:
        led.on()
        time.sleep(2)
        led.off()
    finally:
        led.close()
        print("LED test finished")
