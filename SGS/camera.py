from __future__ import annotations
import cv2, threading, time
from .config import CONFIG
from .detection import VisionDetector, draw_detections

class CameraStream:
    def __init__(self, source: str = CONFIG.camera_url):
        self.source = source
        self.detector = VisionDetector()
        self.frame = None
        self.detections = []
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._loop, daemon=True).start()

    def _open(self):
        cap = cv2.VideoCapture(self.source)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        return cap

    def _loop(self):
        cap = self._open(); last_detect = 0
        while self.running:
            ok, frame = cap.read()
            if not ok:
                cap.release(); time.sleep(1); cap = self._open(); continue
            if time.time() - last_detect > 0.25:
                self.detections = self.detector.detect(frame)
                last_detect = time.time()
            annotated = draw_detections(frame.copy(), self.detections)
            with self.lock: self.frame = annotated
        cap.release()

    def latest(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy(), list(self.detections)
