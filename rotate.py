import threading
import time

class Rotator:
    def __init__(self):
        self.running = True
        # Initialize the thread
        self.rotation_thread = threading.Thread(target=self._run_rotation, daemon=True)
        
    def start(self):
        self.rotation_thread.start()
        
    def _run_rotation(self):
        while self.running:
            print("Rotating...")
            time.sleep(1) # Replace with your rotation logic
            
    def stop(self):
        self.running = False
        self.rotation_thread.join()