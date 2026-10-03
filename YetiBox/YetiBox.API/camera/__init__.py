from dataclasses import dataclass
from typing import Protocol
import queue

@dataclass
class OpenCvConfig:
    ''' Index of the camera to use '''
    camera_index: int = 0

    ''' Should the video stream be displayed locally for testing '''
    local_display: bool = False

''' Interface for a camera '''
class ICamera(Protocol):
    ''' Constructor '''
    def __init__(self, data_queue):
        self.data_queue = data_queue
        pass

    ''' Main entry point to run the entire IStream infrastructure '''
    def run(self) -> None:
        while (True):
            data = self.get_data()
            try:
                self.data_queue.put_nowait(data)
            except queue.Full:
                self.clear()

                # If it fails again...just fail it.
                self.data_queue.put_nowait(data)

    ''' Clears any held data '''
    def clear(self) -> None:
        try:    
            _ = self.data_queue.get_nowait()
        except queue.Empty:
            pass


from .network_camera import NetworkCamera
from .test_camera import TestCamera
from .usb_camera import UsbCamera

