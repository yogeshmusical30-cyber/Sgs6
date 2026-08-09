from __future__ import annotations
from collections import deque
from datetime import datetime

class ActivityLogger:
    def __init__(self, limit: int = 80):
        self.events = deque(maxlen=limit)
        self.info("SGS boot sequence initialized")

    def info(self, message: str) -> None:
        self.events.appendleft(f"[{datetime.now():%H:%M:%S}] {message}")

    def latest(self, count: int = 8) -> list[str]:
        return list(self.events)[:count]
