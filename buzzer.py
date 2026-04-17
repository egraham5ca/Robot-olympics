import time
from gpiozero import OutputDevice

class Buzzer:
    def __init__(self):
        self.PIN = 17  # BCM 17
        self.buzzer_pin = OutputDevice(
            self.PIN,
            active_high=False,   # ✅ CRITICAL FIX
            initial_value=False
        )

    def set_state(self, state: bool) -> None:
        self.buzzer_pin.on() if state else self.buzzer_pin.off()

    def close(self) -> None:
        self.buzzer_pin.off()
        self.buzzer_pin.close()
        
if __name__ == '__main__':
    print('Program is starting ... ')     # Print a message indicating the start of the program
    buzzer = Buzzer()                     # Create an instance of the Buzzer class
    try:
        for _ in range(3):
            buzzer.set_state(True)        # Turn on the buzzer
            time.sleep(0.1)               # Wait for 0.1 second
            buzzer.set_state(False)       # Turn off the buzzer
            time.sleep(0.1)               # Wait for 0.1 second
    finally:
        buzzer.close()                    # Ensure the buzzer pin is closed when the program is interrupted
        print("\nEnd of program")
