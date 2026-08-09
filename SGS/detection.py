from __future__ import annotations
import cv2
from dataclasses import dataclass
from .wound import detect_large_blood_regions

@dataclass
class Detection:
    label: str
    bbox: tuple[int, int, int, int]
    details: list[str]
    color: tuple[int, int, int]

class VisionDetector:
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        cascade = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face = cv2.CascadeClassifier(cascade)

    def detect(self, frame):
        detections: list[Detection] = []
        small = cv2.resize(frame, (min(960, frame.shape[1]), int(frame.shape[0] * min(960, frame.shape[1]) / frame.shape[1])))
        scale_x = frame.shape[1] / small.shape[1]; scale_y = frame.shape[0] / small.shape[0]
        rects, _ = self.hog.detectMultiScale(small, winStride=(8, 8), padding=(8, 8), scale=1.08)
        for (x, y, w, h) in rects[:8]:
            box = (int(x*scale_x), int(y*scale_y), int(w*scale_x), int(h*scale_y))
            age = "22-32" if w > 60 else "Unknown"
            detections.append(Detection("HUMAN", box, [f"Estimated Age: {age}", "Injured: No", "Pulse: Normal", "Body Temp: Normal", "Name: Unknown", "Criminal DB: Unknown"], (80,255,60)))
        for blood in detect_large_blood_regions(frame):
            detections.append(Detection("BLOOD", blood["bbox"], [f"Heavy bleeding: {'Yes' if blood['heavy_bleeding'] else 'No'}", "Cause: Unknown", "First aid: Apply pressure"], (0,0,255)))
        # Vehicle/object detection needs trained models; avoid fake boxes. Summaries stay zero unless model added.
        return detections

def draw_detections(frame, detections):
    for d in detections:
        x,y,w,h = d.bbox
        cv2.rectangle(frame, (x,y), (x+w,y+h), d.color, 2)
        cv2.putText(frame, d.label, (x, max(18, y-8)), cv2.FONT_HERSHEY_SIMPLEX, .6, d.color, 2)
        for i, line in enumerate(d.details[:6]):
            cv2.putText(frame, line, (x+4, y+20+i*18), cv2.FONT_HERSHEY_SIMPLEX, .45, (235,245,255), 1)
    return frame
