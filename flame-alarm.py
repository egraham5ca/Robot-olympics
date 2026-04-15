#!/usr/bin/python3
# Flame Alarm Automatic Drive-Away System
# Robot Olympics – Raspberry Pi 4B
# Author: Emma Graham

import RPi.GPIO as GPIO
import time
from car import Car

# =========================
# CONFIGURATION
# =========================
FLAME_PIN = 24          # BCM pin for flame sensor
CHECK_INTERVAL = 0.1   # seconds
BACK_SPEED = 40        # motor speed %
ROTATE_SPEED = 30
BACK_TIME = 0.6        # seconds
ROTATE_TIME = 0.4

# =========================
# INITIALIZATION
# =========================
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)

car = Car()

print("[SYSTEM] Flame avoidance system started")

# =========================
# FUNCTIONS
# =========================
def flame_detected():
    """
    Flame sensors typically output LOW when fire is detected
    """
    return GPIO.input(FLAME_PIN) == GPIO.LOW


def move_away_from_fire():
    """
    Simple and reliable escape behavior:
    1. Stop
    2. Move backward
    3. Rotate to escape flame cone
    """
    print("🔥 FIRE DETECTED — EVADING")

    car.stop()
    time.sleep(0.1)

    # Move backward
    car.move_backward(BACK_SPEED)
    time.sleep(BACK_TIME)

    # Rotate right to change direction
    car.rotate_right(ROTATE_SPEED)
    time.sleep(ROTATE_TIME)

    car.stop()
    print("[SYSTEM] Evade maneuver complete")


# =========================
# MAIN LOOP
# =========================
try:
    while True:
        if flame_detected():
            move_away_from_fire()
            time.sleep(0.5)  # cooldown to avoid jitter
        else:
            time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n[SYSTEM] Shutdown requested by user")

finally:
    car.stop()
    GPIO.cleanup()
    print("[SYSTEM] GPIO cleaned up, motors stopped")
