import queue
import time
from pathlib import Path

import cv2


""" A camera for streaming a static test image. """
class TestCamera:
    """ Constructor """
    def __init__(self, data_queue: queue.Queue) -> None:
        self.data_queue = data_queue
        self.ready = False
        image_path = Path(__file__).resolve().parents[3] / "Project Files" / "logo.png"
        self.test_image = cv2.imread(str(image_path))
        if self.test_image is None:
            raise FileNotFoundError(f"Unable to load test image: {image_path}")

    def run(self) -> None:
        self.ready = True
        frame_interval = 1 / 30
        next_frame_time = time.monotonic()
        while (True):
            data = self.get_data()
            try:
                self.data_queue.put_nowait(data)
            except queue.Full:
                self.clear()

                # If it fails again...just fail it.
                self.data_queue.put_nowait(data)

            next_frame_time += frame_interval
            time.sleep(max(0, next_frame_time - time.monotonic()))

    def clear(self) -> None:
        try:    
            _ = self.data_queue.get_nowait()
        except queue.Empty:
            pass

    def get_data(self):
        return self.test_image.copy()
