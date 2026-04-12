import threading
import time
import math

class Rotator:
    """Test class for rotating the Mecanum car"""
    
    def __init__(self, car, target_angle=360, speed=50):
        """
        Initialize rotator
        
        Args:
            car: Car object with motor control
            target_angle: Degrees to rotate (360 = full rotation)
            speed: Motor speed (0-255)
        """
        self.car = car
        self.target_angle = target_angle
        self.speed = speed
        self.running = False
        self.rotation_thread = None
        self.current_angle = 0
        self.start_time = None
        
    def start(self):
        """Start rotation in a separate thread"""
        if self.running:
            print("Rotation already running!")
            return
            
        self.running = True
        self.current_angle = 0
        self.start_time = time.time()
        self.rotation_thread = threading.Thread(target=self._run_rotation, daemon=False)
        self.rotation_thread.start()
        print(f"[ROTATE] Starting rotation: {self.target_angle}° at speed {self.speed}")
        
    def _run_rotation(self):
        """Main rotation logic - runs in separate thread"""
        try:
            while self.running and self.current_angle < self.target_angle:
                # Set motors for rotation (all motors same direction)
                # For Mecanum: rotating in place requires specific motor pattern
                self.car.motor.set_motor_model(
                    self.speed,   # Front Left
                    self.speed,   # Back Left
                    -self.speed,  # Front Right (opposite direction)
                    -self.speed   # Back Right (opposite direction)
                )
                
                # Simulate angle progress (replace with actual sensor data)
                elapsed = time.time() - self.start_time
                self.current_angle = (elapsed * 90) % self.target_angle  # ~90°/sec
                
                print(f"[ROTATE] Angle: {self.current_angle:.1f}° / {self.target_angle}°")
                time.sleep(0.1)
            
            # Stop motors when done
            if self.current_angle >= self.target_angle:
                self.car.motor.set_motor_model(0, 0, 0, 0)
                print(f"[ROTATE] ✓ Rotation complete! Final angle: {self.current_angle:.1f}°")
            
        except Exception as e:
            print(f"[ROTATE] ✗ Error during rotation: {e}")
        finally:
            self.running = False
            
    def stop(self):
        """Stop rotation immediately"""
        if not self.running:
            return
            
        self.running = False
        self.car.motor.set_motor_model(0, 0, 0, 0)  # Stop motors
        
        if self.rotation_thread and self.rotation_thread.is_alive():
            self.rotation_thread.join(timeout=1.0)
        
        print(f"[ROTATE] Stopped at angle: {self.current_angle:.1f}°")
        
    def is_running(self):
        """Check if rotation is active"""
        return self.running
    
    def get_angle(self):
        """Get current rotation angle"""
        return self.current_angle


# Example usage / Test code
if __name__ == "__main__":
    from car import Car
    
    try:
        # Initialize car
        car = Car()
        print("[TEST] Car initialized")
        
        # Test 1: Full 360° rotation
        print("\n[TEST] Test 1: Full 360° rotation")
        rotator = Rotator(car, target_angle=360, speed=80)
        rotator.start()
        
        # Monitor rotation
        while rotator.is_running():
            time.sleep(0.5)
        
        time.sleep(1)
        
        # Test 2: 90° rotation
        print("\n[TEST] Test 2: 90° rotation")
        rotator2 = Rotator(car, target_angle=90, speed=100)
        rotator2.start()
        
        while rotator2.is_running():
            time.sleep(0.5)
        
        # Test 3: Stop mid-rotation
        print("\n[TEST] Test 3: Stop mid-rotation")
        rotator3 = Rotator(car, target_angle=360, speed=60)
        rotator3.start()
        time.sleep(2)
        rotator3.stop()
        print(f"Stopped at: {rotator3.get_angle():.1f}°")
        
        print("\n[TEST] All tests completed!")
        car.close()
        
    except KeyboardInterrupt:
        print("\n[TEST] Interrupted by user")
        car.motor.set_motor_model(0, 0, 0, 0)
        car.close()
    except Exception as e:
        print(f"\n[TEST] Error: {e}")
        car.close()
