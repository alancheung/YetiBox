import multiprocessing as mp
from queue import Queue as ThreadQueue
from threading import Thread
from time import sleep

from camera import CameraConfig, CameraType, ICamera, UsbCamera


class CameraWorker(mp.Process):
    def __init__(self, config: CameraConfig, raw_queue: mp.Queue, processed_queue: mp.Queue):
        super().__init__()
        # Exits on crash
        self.daemon = True

        # Before image processing as fast as possible
        self.raw_queue = raw_queue
        self.processed_queue = processed_queue
        self.camera_thread = self.__setup_io_thread(config)

    def run(self) -> None:
        ''' The main work process loop.
        1. Read unprocessed frame via a dedicated camera thread.
        2. Run OpenCV on unprocessed frame creating a processed frame
        3. Output the processed frame.
        '''
        self.camera_thread.start()
        
        try:
            while True:
                # Make the raw frame available ASAP for viewers
                raw_frame = self.input_queue.get_nowait()
                _ = self.raw_queue.get_nowait()
                self.raw_queue.put_nowait(raw_frame)
                
                processed_frame = self.process_frame(raw_frame)
                _ = self.processed_queue.get_nowait()
                self.processed_queue.put_nowait(processed_frame)
        except BaseException as ex:
            print(f"Exception encountered in camera worker! Exception {ex}")
            pass

    def __setup_io_thread(self, config: CameraConfig) -> Thread:
        ''' Setup the IO thread to input unprocessed frames '''
        self.input_queue = ThreadQueue(maxsize=1)
        self.camera = self.__create_camera(self.input_queue, config);
        return Thread(name="Camera Thread", target=self.camera.run)
    
    def __create_camera(self, input_queue: ThreadQueue, config: CameraConfig) -> ICamera:
        ''' Initializes the camera used by this worker '''
        match config.camera_type:
            case CameraType.USB:
                return UsbCamera(data_queue=input_queue, config=config)
            case _:
                raise ValueError(f"Camera of type {config.camera_type} is unsupported!")

    def process_frame():
        print('Processed frame in worker')
        sleep(2)
        pass



