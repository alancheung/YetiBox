from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol
import queue

class CameraType(Enum):
    ''' The types of camera applications that could be used. '''
    TEST =  1
    OPENCV = 2
    

@dataclass
class CameraConfig:
    camera_type: CameraType = CameraType.OPENCV

    ''' Index of the camera to use '''
    camera_name: str = "rtsp://yetibox-camera:8554/cam"

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


from .test_camera import TestCamera
from .opencv_camera import OpenCvCamera
from .worker import CameraWorker

