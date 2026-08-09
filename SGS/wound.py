from __future__ import annotations
import cv2
import numpy as np

MIN_BLOOD_AREA_RATIO = 0.018  # ignore tiny red marks/noise
MIN_CONTOUR_AREA = 1800

def detect_large_blood_regions(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 70, 55]); upper1 = np.array([9, 255, 255])
    lower2 = np.array([170, 70, 55]); upper2 = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = frame.shape[:2]
    detections = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < MIN_CONTOUR_AREA or area / (w * h) < MIN_BLOOD_AREA_RATIO:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        detections.append({"label": "Blood", "bbox": (x, y, bw, bh), "area": int(area), "heavy_bleeding": area / (w*h) > 0.045})
    return detections
