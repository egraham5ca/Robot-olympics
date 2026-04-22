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

ESCAPE_DURATION = 2  # seconds
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
        now = time.time()  # ✅ GET CURRENT TIME

        # Keyestudio behavior:
        # LOW  = flame detected
        # HIGH = no flame
        if flame_state == GPIO.LOW and not escaping:  # ✅ ONLY START IF NOT ALREADY ESCAPING
            print("🔥 FIRE DETECTED — ESCAPING")
            escaping = True  # ✅ SET ESCAPE FLAG
            last_escape_time = now  # ✅ RECORD START TIME

            # Move backward (all wheels reverse)
            car.set_motor_model(
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED
            )
        
        # ✅ FIX: PROPER ESCAPE DURATION LOGIC
        if escaping and (now - last_escape_time) >= ESCAPE_DURATION:
            escaping = False
            car.set_motor_model(0, 0, 0, 0)
            print("✅ Escape complete")

        # ✅ FIX: STOP IF NO FLAME AND NOT ESCAPING
        if flame_state == GPIO.HIGH and not escaping:
            car.set_motor_model(0, 0, 0, 0)

        time.sleep(CHECK_DELAY)  # ✅ INDENTED CORRECTLY


except KeyboardInterrupt:
    print("\n[SYSTEM] Program stopped by user")

finally:
    car.set_motor_model(0, 0, 0, 0)
    car.close()
    GPIO.cleanup()
    print("[SYSTEM] Motors stopped, GPIO cleaned up")
