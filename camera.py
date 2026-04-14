import cv2
import time
from threading import Condition
import io

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf: bytes) -> int:
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
        return len(buf)


class Camera:
    def __init__(self, preview_size=(640, 480), hflip=False, vflip=False, stream_size=(400, 300)):
        self.preview_size = preview_size
        self.stream_size = stream_size
        self.hflip = hflip
        self.vflip = vflip

        # Open USB camera
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("ERROR: USB camera could not be opened")

        # Try to set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, preview_size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, preview_size[1])

        # Allow camera to respond
        time.sleep(0.2)

        # Read back actual resolution
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # If camera ignored the request, fallback to 320x240
        if w == 0 or h == 0:
            print("WARNING: Camera did not accept resolution, falling back to 320x240")
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.streaming_output = StreamingOutput()
        self.streaming = False

    def start_image(self):
        # USB cameras do not need preview start
        pass

    def save_image(self, filename: str):
        ret, frame = self.cap.read()
        if not ret:
            print("ERROR: Could not read frame from USB camera")
            return None

        # Apply flips
        if self.hflip:
            frame = cv2.flip(frame, 1)
        if self.vflip:
            frame = cv2.flip(frame, 0)

        cv2.imwrite(filename, frame)
        return {"saved": filename}

    def start_stream(self, filename=None):
        self.streaming = True

    def stop_stream(self):
        self.streaming = False

    def get_frame(self) -> bytes:
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Resize to stream size
        frame = cv2.resize(frame, self.stream_size)

        # Apply flips
        if self.hflip:
            frame = cv2.flip(frame, 1)
        if self.vflip:
            frame = cv2.flip(frame, 0)

        # Encode as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return None

        return jpeg.tobytes()

    def save_video(self, filename: str, duration: int = 10):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename, fourcc, 20.0, self.preview_size)

        start = time.time()
        while time.time() - start < duration:
            ret, frame = self.cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()

    def close(self):
        self.cap.release()
