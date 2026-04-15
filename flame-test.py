#!/usr/bin/python3
# ============================================
# Flame Sensor Potentiometer Debug Test
# Keyestudio Flame Sensor (Digital Output D0)
# Raspberry Pi 4B
# ============================================

import time
import RPi.GPIO as GPIO

FLAME_PIN = 16  # BCM pin connected to D0

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)

print("====================================")
print("Flame Sensor Potentiometer Debug")
print("Watching GPIO", FLAME_PIN)
print("Turn the potentiometer SLOWLY.")
print("You should see the value change.")
print("====================================")

last_state = None

try:
    while True:
        state = GPIO.input(FLAME_PIN)

        # Print every time the state changes
        if state != last_state:
            if state == GPIO.LOW:
                print("GPIO 24 = LOW  🔥 (FLAME / BELOW THRESHOLD)")
            else:
                print("GPIO 24 = HIGH ✅ (NO FLAME / ABOVE THRESHOLD)")
            last_state = state

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting debug test")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
