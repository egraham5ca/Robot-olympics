from adc import ADC
import time

class Photoresistor:
    def __init__(self):
        """Initialize the Photoresistor class and create an ADC instance."""
        self.adc = ADC()

    def read_left_photoresistor(self) -> float:
        """Read the value from the left photoresistor."""
        try:
            return self.adc.read_adc(0)  # Changed from recvADC to read_adc
        except Exception as e:
            print(f"Error reading left photoresistor: {e}")
            return None

    def read_right_photoresistor(self) -> float:
        """Read the value from the right photoresistor."""
        try:
            return self.adc.read_adc(1)  # Changed from recvADC to read_adc
        except Exception as e:
            print(f"Error reading right photoresistor: {e}")
            return None

    def stop(self) -> None:
        """Close the I2C bus."""
        self.adc.close_i2c()  # Also changed from i2cClose() to close_i2c()

if __name__ == '__main__':
    print('Program is starting ... ')
    photoresistor = Photoresistor()
    try:
        while True:
            left_value = photoresistor.read_left_photoresistor()
            right_value = photoresistor.read_right_photoresistor()
            if left_value is not None and right_value is not None:
                print(f"The photoresistor L is {left_value}V, R is {right_value}V")
            time.sleep(0.3)
    except KeyboardInterrupt:
        print('\nProgram is stopped! ')
        photoresistor.stop()
