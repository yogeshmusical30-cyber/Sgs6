from __future__ import annotations

import threading
import time
from typing import List, Optional, Tuple

from .compat import optional_import
from .config import CONFIG
from .detection import Detection, VisionDetector, draw_detections

cv2 = optional_import("cv2")


class CameraStream:
    def __init__(self, source: str = CONFIG.camera_url):
        self.source = source
        self.detector = VisionDetector()
        self.frame = None
        self.detections: List[Detection] = []
        self.running = False
        self.lock = threading.Lock()
        self.error = ""

    def start(self) -> None:
        if not self.running:
            self.running = True
            threading.Thread(target=self._loop, daemon=True).start()

    def stop(self) -> None:
        self.running = False

    def _open(self):
        if cv2 is None:
            self.error = "OpenCV is not installed. Run: pip install -r requirements.txt"
            return None
        cap = cv2.VideoCapture(self.source)
        try:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            pass
        return cap

    def _loop(self) -> None:
        cap = self._open()
        last_detect = 0.0
        while self.running:
            if cap is None:
                time.sleep(1)
                cap = self._open()
                continue
            ok, frame = cap.read()
            if not ok or frame is None:
                self.error = "Waiting for AirDroid feed at {}".format(self.source)
                try:
                    cap.release()
                except Exception:
                    pass
                time.sleep(1)
                cap = self._open()
                continue
            self.error = ""
            if time.time() - last_detect > 0.25:
                self.detections = self.detector.detect(frame)
                last_detect = time.time()
            annotated = draw_detections(frame.copy(), self.detections)
            with self.lock:
                self.frame = annotated
        try:
            cap.release()
        except Exception:
            pass

    def latest(self) -> Tuple[Optional[object], List[Detection], str]:
        with self.lock:
            frame = None if self.frame is None else self.frame.copy()
            return frame, list(self.detections), self.error
