from dataclasses import dataclass
from typing import Protocol
import queue

from settings import CameraType

class ICamera(Protocol):
    """ 
    Interface for a camera at least as much as Python can get. Works via duck typing
    """
    def __init__(self, data_queue):
        """ Constructor that accepts the data_queue to return frames on """
        self.data_queue = data_queue
        pass

    def run(self) -> None:
        """ Main entry point to run. """
        pass

    def clear(self) -> None:
        """ Clears any held data in the queue """
        pass


from .test_camera import TestCamera
from .opencv_camera import OpenCvCamera
from .worker import CameraWorker
