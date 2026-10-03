import time
import queue

''' A class for streaming data retrieved from the network'''
class TestCamera:
    ''' Constructor '''
    def __init__(self, data_queue: queue.Queue) -> None:
        self.data_queue = data_queue
        self.counter = 0

    def run(self) -> None:
        while (True):
            data = self.get_data()
            try:
                self.data_queue.put_nowait(data)
            except queue.Full:
                self.clear()

                # If it fails again...just fail it.
                self.data_queue.put_nowait(data)

    def clear(self) -> None:
        try:    
            _ = self.data_queue.get_nowait()
        except queue.Empty:
            pass
    
    def get_data(self) -> str:
        message = f"test_stream: {self.counter}"
        self.counter += 1
        time.sleep(1)
        print(message);
        return message




