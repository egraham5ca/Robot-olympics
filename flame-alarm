import RPi.GPIO as GPIO
import time

FLAME_PIN = 24  # BCM

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(FLAME_PIN) == GPIO.LOW:
            print("🔥 Flame detected")
        else:
            print("No flame")
        time.sleep(0.2)
finally:
    GPIO.cleanup()
