from typing import Protocol
from .network_streamer import NetworkStreamer
from .test_streamer import TestStreamer

''' Interface for a streamer '''
class IStreamer(Protocol):
    def run(self) -> None:
        pass

    ''' Clears any held data '''
    def clear(self) -> None:
        pass

    ''' Gets any data available '''
    def get_data(self):
        pass
    
