import queue
import cv2
from settings import CameraConfig


""" ICamera that retrieves camera images using OpenCV and makes them available """
class OpenCvCamera():
    """ Constructor """
    def __init__(self, data_queue: queue.Queue, config: CameraConfig):
        self.data_queue = data_queue
        self.config = config
        self.ready = False
        pass

    """ Initializes the camera and begins capturing frames from it in a loop. """
    def run(self) -> None:
        # Allow them to pass either '0' (for USB) or a string for network cameras.
        parsed_camera_name = self.config.camera_name
        try:
            parsed_camera_name = int(parsed_camera_name)
        except (ValueError, TypeError):
            pass # Hopefully it's a string name so continue

        self.camera = cv2.VideoCapture(parsed_camera_name)
        if not self.camera.isOpened():
            print("Camera is not open!")
            raise RuntimeError(f"Camera at {parsed_camera_name} is not available!");
        self.ready = True

        while (True):
            read, frame = self.camera.read()
            if self.config.local_display:
                cv2.imshow('Camera', frame)
                cv2.waitKey(1)

            try:
                self.data_queue.put_nowait(frame)
            except queue.Full:
                self.clear()

                # If it fails again...just fail it.
                self.data_queue.put_nowait(frame)
                
    """ Clears any held data """
    def clear(self) -> None:
        try:    
            _ = self.data_queue.get_nowait()
        except queue.Empty:
            pass