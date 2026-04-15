#!/usr/bin/python3
# ============================================
# Flame Alarm Auto-Escape Program
# Robot Olympics – Raspberry Pi 4B
# Uses PCA9685 motor driver + flame sensor
# ============================================

import time
import RPi.GPIO as GPIO
from pca9685 import PCA9685

# ============================================
# CONFIGURATION
# ============================================
FLAME_PIN = 24        # BCM pin for flame sensor
CHECK_DELAY = 0.05   # seconds between checks

# Motor behavior (0–4095) — KEEP SAME SPEED
ESCAPE_SPEED = 2000

# ============================================
# MOTOR CLASS (CORRECTED)
# ============================================
class Ordinary_Car:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.set_pwm_freq(50)

    def duty_range(self, d1, d2, d3, d4):
        return (
            max(min(d1, 4095), -4095),
            max(min(d2, 4095), -4095),
            max(min(d3, 4095), -4095),
            max(min(d4, 4095), -4095),
        )

    def left_upper_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(0, 0)
            self.pwm.set_motor_pwm(1, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(1, 0)
            self.pwm.set_motor_pwm(0, abs(duty))
        else:
            self.pwm.set_motor_pwm(0, 0)
            self.pwm.set_motor_pwm(1, 0)

    def left_lower_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(3, 0)
            self.pwm.set_motor_pwm(2, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(2, 0)
            self.pwm.set_motor_pwm(3, abs(duty))
        else:
            self.pwm.set_motor_pwm(2, 0)
            self.pwm.set_motor_pwm(3, 0)

    def right_upper_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(6, 0)
            self.pwm.set_motor_pwm(7, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(7, 0)
            self.pwm.set_motor_pwm(6, abs(duty))
        else:
            self.pwm.set_motor_pwm(6, 0)
            self.pwm.set_motor_pwm(7, 0)

    def right_lower_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(4, 0)
            self.pwm.set_motor_pwm(5, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(5, 0)
            self.pwm.set_motor_pwm(4, abs(duty))
        else:
            self.pwm.set_motor_pwm(4, 0)
            self.pwm.set_motor_pwm(5, 0)

    def set_motor_model(self, d1, d2, d3, d4):
        d1, d2, d3, d4 = self.duty_range(d1, d2, d3, d4)
        self.left_upper_wheel(d1)
        self.left_lower_wheel(d2)
        self.right_upper_wheel(d3)
        self.right_lower_wheel(d4)

    def stop(self):
        # HARD STOP — guarantees motors off
        for ch in range(8):
            self.pwm.set_motor_pwm(ch, 0)

    def close(self):
        self.stop()
        self.pwm.close()

# ============================================
# FLAME SENSOR SETUP
# ============================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)

car = Ordinary_Car()

print("[SYSTEM] Flame alarm auto-escape active")

# ============================================
# MAIN LOOP
# ============================================
try:
    while True:
        if GPIO.input(FLAME_PIN) == GPIO.LOW:
            # FIRE DETECTED → KEEP MOVING
            print("🔥 FIRE DETECTED — ESCAPING")
            car.set_motor_model(
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED,
                -ESCAPE_SPEED
            )
        else:
            # NO FIRE → STOP
            car.stop()

        time.sleep(CHECK_DELAY)

except KeyboardInterrupt:
    print("\n[SYSTEM] Program stopped by user")

finally:
    car.close()
    GPIO.cleanup()
    print("[SYSTEM] Motors stopped, GPIO cleaned up")
