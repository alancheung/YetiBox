from typing import Protocol
import queue

''' Interface for a streamer '''
class IStreamer(Protocol):
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


from .network_streamer import NetworkStreamer
from .test_streamer import TestStreamer
from .usb_streamer import UsbStreamer, UsbCameraConfig

