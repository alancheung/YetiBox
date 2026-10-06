from datetime import datetime
import multiprocessing as mp
from queue import Queue as ThreadQueue, Empty as QueueEmpty, Full as QueueFull
from threading import Thread
from time import sleep, time

import cv2

from camera import CameraType, ICamera, OpenCvCamera
from settings import CameraConfig
from homeassistant import HomeAssistantGateway

class CameraWorker(mp.Process):
    def __init__(self, config: CameraConfig, raw_queue: mp.Queue, processed_queue: mp.Queue, gateway: HomeAssistantGateway):
        super().__init__()
        # Exits on crash
        self.daemon = True

        self.config = config
        self.raw_queue = raw_queue
        self.processed_queue = processed_queue
        self.gateway = gateway

        self.last_detection: tuple[float, str] = [time.monotonic(), '']

    def run(self) -> None:
        ''' The main work process loop.
        1. Read unprocessed frame via a dedicated camera thread.
        2. Run OpenCV on unprocessed frame creating a processed frame
        3. Output the processed frame.
        '''
        self.camera_thread = self.__setup_io_thread(self.config)
        self.camera_thread.start()
        self.qr_detector = cv2.QRCodeDetector()
        
        try:
            while True:
                if not self.camera.ready:
                    continue

                try:
                    raw_frame = self.input_queue.get_nowait()

                    # Make the raw frame available ASAP for viewers
                    self._put_frame(self.raw_queue, raw_frame)
                except QueueEmpty:
                    continue # skips instead of pass
                
                try:
                    processed_frame, data = self._process_frame(raw_frame)
                    self._handle_detection(detected_data=data)
                    self._put_frame(self.processed_queue, processed_frame)
                    
                    if self.config.local_display:
                        cv2.imshow('Worker', processed_frame)
                        cv2.waitKey(1)
                except QueueEmpty:
                    continue # skips instead of pass
        except BaseException as ex:
            print(f"Exception encountered in camera worker! Exception {ex}")

    def __setup_io_thread(self, config: CameraConfig) -> Thread:
        ''' Setup the IO thread to input unprocessed frames '''
        self.input_queue = ThreadQueue(maxsize=1)
        self.camera = self.__create_camera(self.input_queue, config);
        return Thread(name="Camera Thread", target=self.camera.run)
    
    def __create_camera(self, input_queue: ThreadQueue, config: CameraConfig) -> ICamera:
        ''' Initializes the camera used by this worker '''
        match config.camera_type:
            case CameraType.OPENCV:
                return OpenCvCamera(data_queue=input_queue, config=config)
            case _:
                raise ValueError(f"Camera of type {config.camera_type} is unsupported!")

    def _process_frame(self, frame):
        data, bbox, _ = self.qr_detector.detectAndDecode(frame)

        detected_data = data if bbox is not None and data else None
        if detected_data:
            bbox = bbox.astype(int)
            cv2.polylines(frame, [bbox], isClosed=True, color=(0, 255, 0), thickness=3)
            cv2.putText(frame, text=f"QR '{data}' {self.TODO_TEST}! {datetime.now()}", org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        else:
            cv2.putText(frame, text=f"Processed {datetime.now()}", org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        return frame, detected_data

    def _handle_detection(self, detected_data: str) -> None:
        """ Take action when a valid code has been detected """
        last_timestamp, last_data = self.last_detection
        if last_data != detected_data or time.monotonic() - last_timestamp > self.config.last_detection_valid_secs:
            match detected_data:
                case _:
                    self.gateway.toggle_light_test()

    @staticmethod
    def _put_frame(queue: mp.Queue, frame) -> None:
        try:
            queue.put_nowait(frame)
        except QueueFull:
            try:
                queue.get_nowait()
            except QueueEmpty:
                # This is an interesting case. We're only intending one consumer of this queue.
                # The consumer is not also a producer so the only interaction between this class and a consumer
                # is when the consumer takes the frame after the detection here that the queue is full.
                # Since we are also attempting to free the queue just ignore it if it was stolen. 
                # Assume that the consumer handles if the get_nowait() handles their frame stolen
                # Put the next one here, we don't care if they get it or not.
                pass 
            queue.put_nowait(frame)


