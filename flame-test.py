#!/usr/bin/python3
# ============================================
# Flame Alarm Auto-Escape Program
# Robot Olympics – Raspberry Pi 4B

import time
import RPi.GPIO as GPIO
from motor import Ordinary_Car

# ============================================
# CONFIGURATION
# ============================================
FLAME_PIN = 16          # ✅ confirmed working pin
BUZZER_PIN = 18         # BCM pin for active buzzer

CHECK_DELAY = 0.05      # loop delay (seconds)

ESCAPE_SPEED = 2000     # keep same speed
ESCAPE_DURATION = 0.7  # seconds (reverse time)
TURN_DURATION = 0.4    # seconds (rotate time)

# ============================================
# SETUP
# ============================================
GPIO.setmode(GPIO.BCM)

GPIO.setup(FLAME_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

car = Ordinary_Car()

escaping = False
escape_stage = 0        # 0 = idle, 1 = reverse, 2 = turn
stage_start_time = 0

print("[SYSTEM] Flame alarm auto-escape active")
print("[SYSTEM] Flame sensor on GPIO 16 (ACTIVE-LOW)")
print("[SYSTEM] Buzzer on GPIO 18")

# ============================================
# MAIN LOOP
# ============================================
try:
    while True:
        flame_state = GPIO.input(FLAME_PIN)
        now = time.time()

        # ====================================
        # FIRE DETECTED (ACTIVE-LOW)
        # ====================================
        if flame_state == GPIO.LOW and not escaping:
            print("🔥 FIRE DETECTED — ESCAPING")
            escaping = True
            escape_stage = 1
            stage_start_time = now

            GPIO.output(BUZZER_PIN, GPIO.HIGH)

            # Stage 1: reverse
            car.set_motor_model(
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED
            )

        # ====================================
        # ESCAPE SEQUENCE
        # ====================================
        if escaping:
            # Stage 1 → reverse
            if escape_stage == 1 and (now - stage_start_time) >= ESCAPE_DURATION:
                escape_stage = 2
                stage_start_time = now

                # Stage 2: rotate right
                car.set_motor_model(
                    ESCAPE_SPEED,
                    ESCAPE_SPEED,
                    -ESCAPE_SPEED,
                    -ESCAPE_SPEED
                )

            # Stage 2 → finish
            elif escape_stage == 2 and (now - stage_start_time) >= TURN_DURATION:
                escaping = False
                escape_stage = 0

                car.set_motor_model(0, 0, 0, 0)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                print("✅ Escape complete")

        # ====================================
        # NO FIRE & NOT ESCAPING
        # ====================================
        if flame_state == GPIO.HIGH and not escaping:
            car.set_motor_model(0, 0, 0, 0)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(CHECK_DELAY)

except KeyboardInterrupt:
    print("\n[SYSTEM] Program stopped by user")

finally:
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    car.set_motor_model(0, 0, 0, 0)
    car.close()
    GPIO.cleanup()
    print("[SYSTEM] Motors stopped, GPIO cleaned up")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
