import time
import queue

class NetworkStreamer:
    ''' Constructor '''
    def __init__(self, data_queue: queue.Queue) -> None:
        self.data_queue = data_queue
        self.counter = 0

    def run(self) -> None:
        pass    
    
    def get_data(self) -> str:
        pass




