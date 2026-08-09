from __future__ import annotations

from typing import List
from .compat import optional_import

cv2 = optional_import("cv2")
np = optional_import("numpy")

MIN_BLOOD_AREA_RATIO = 0.018  # ignore tiny red marks/noise
MIN_CONTOUR_AREA = 1800


def detect_large_blood_regions(frame) -> List[dict]:
    if cv2 is None or np is None or frame is None:
        return []
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower1 = np.array([0, 70, 55])
        upper1 = np.array([9, 255, 255])
        lower2 = np.array([170, 70, 55])
        upper2 = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        h, w = frame.shape[:2]
        detections = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < MIN_CONTOUR_AREA or area / float(w * h) < MIN_BLOOD_AREA_RATIO:
                continue
            x, y, bw, bh = cv2.boundingRect(contour)
            detections.append({
                "label": "Blood",
                "bbox": (x, y, bw, bh),
                "area": int(area),
                "heavy_bleeding": area / float(w * h) > 0.045,
            })
        return detections
    except Exception:
        return []
