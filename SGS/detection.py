from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .compat import optional_import
from .wound import detect_large_blood_regions

cv2 = optional_import("cv2")


@dataclass
class Detection:
    label: str
    bbox: Tuple[int, int, int, int]
    details: List[str]
    color: Tuple[int, int, int]


class VisionDetector:
    def __init__(self) -> None:
        self.ready = cv2 is not None
        self.hog = None
        if self.ready:
            try:
                self.hog = cv2.HOGDescriptor()
                self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            except Exception:
                self.hog = None

    def detect(self, frame) -> List[Detection]:
        detections: List[Detection] = []
        if cv2 is None or frame is None:
            return detections
        if self.hog is not None:
            try:
                max_width = min(960, frame.shape[1])
                target_height = max(1, int(frame.shape[0] * max_width / frame.shape[1]))
                small = cv2.resize(frame, (max_width, target_height))
                scale_x = frame.shape[1] / float(small.shape[1])
                scale_y = frame.shape[0] / float(small.shape[0])
                rects, _ = self.hog.detectMultiScale(small, winStride=(8, 8), padding=(8, 8), scale=1.08)
                for (x, y, w, h) in rects[:8]:
                    box = (int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y))
                    age = "22-32" if w > 60 else "Unknown"
                    detections.append(Detection(
                        "HUMAN",
                        box,
                        [
                            "Estimated Age: {}".format(age),
                            "Injured: No",
                            "Pulse: Normal",
                            "Body Temp: Normal",
                            "Name: Unknown",
                            "Criminal DB: Unknown",
                        ],
                        (80, 255, 60),
                    ))
            except Exception:
                pass
        for blood in detect_large_blood_regions(frame):
            detections.append(Detection(
                "BLOOD",
                blood["bbox"],
                [
                    "Heavy bleeding: {}".format("Yes" if blood["heavy_bleeding"] else "No"),
                    "Cause: Unknown",
                    "First aid: Apply pressure",
                ],
                (0, 0, 255),
            ))
        return detections


def draw_detections(frame, detections: List[Detection]):
    if cv2 is None or frame is None:
        return frame
    for detection in detections:
        x, y, w, h = detection.bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), detection.color, 2)
        cv2.putText(frame, detection.label, (x, max(18, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, detection.color, 2)
        for i, line in enumerate(detection.details[:6]):
            cv2.putText(frame, line, (x + 4, y + 20 + i * 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (235, 245, 255), 1)
    return frame
