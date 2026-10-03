import queue
import cv2
from camera import OpenCvConfig


''' ICamera that retrieves camera images from USB and makes them available '''
class UsbCamera():
    ''' Constructor '''
    def __init__(self, data_queue: queue.Queue, config: OpenCvConfig):
        self.data_queue = data_queue
        self.config = config
        self.ready = False
        pass

    ''' Main entry point to run the entire IStream infrastructure '''
    def run(self) -> None:
        self.camera = cv2.VideoCapture(self.config.camera_index)
        if not self.camera.isOpened():
            print("Camera is not open!")
            return
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
                
    ''' Clears any held data '''
    def clear(self) -> None:
        try:    
            _ = self.data_queue.get_nowait()
        except queue.Empty:
            pass