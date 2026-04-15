#!/usr/bin/python3
# ============================================
# Flame Alarm Auto-Escape Program
# Robot Olympics – Raspberry Pi 4B
#
# Hardware:
#  - Keyestudio flame sensor (DIGITAL, ACTIVE-LOW)
#  - 4WD car using PCA9685 motor driver
#
# Behavior:
#  - Flame detected  -> move away
#  - No flame        -> stop motors
# ============================================

import time
import RPi.GPIO as GPIO
from motor import Ordinary_Car   # ✅ SAME driver as working motor test

# ============================================
# CONFIGURATION
# ============================================
FLAME_PIN = 16        # BCM pin (Keyestudio digital output)
CHECK_DELAY = 0.05   # loop delay (seconds)

# KEEP SAME SPEED (as requested)
ESCAPE_SPEED = 2000  # valid range: 0–4095

# ============================================
# SETUP
# ============================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)

car = Ordinary_Car()

ESCAPE_DURATION = 0.7  # seconds
escaping = False
last_escape_time = 0

print("[SYSTEM] Flame alarm auto-escape active")
print("[SYSTEM] Waiting for flame (ACTIVE-LOW)...")

# ============================================
# MAIN LOOP
# ============================================
try:
    while True:
        flame_state = GPIO.input(FLAME_PIN)

        # Keyestudio behavior:
        # LOW  = flame detected
        # HIGH = no flame
        if flame_state == GPIO.LOW:
            print("🔥 FIRE DETECTED — ESCAPING")

            # Move backward (all wheels reverse)
            car.set_motor_model(
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED
            )
        
 # Keep motors running for ESCAPE_DURATION
        if escaping and (now - last_escape_time) < ESCAPE_DURATION:
            pass  # keep moving
        else:
            escaping = False
            car.set_motor_model(0, 0, 0, 0)

    time.sleep(0.05)


except KeyboardInterrupt:
    print("\n[SYSTEM] Program stopped by user")

finally:
    car.set_motor_model(0, 0, 0, 0)
    car.close()
    GPIO.cleanup()
    print("[SYSTEM] Motors stopped, GPIO cleaned up")
