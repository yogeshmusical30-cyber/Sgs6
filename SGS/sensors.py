from __future__ import annotations
import math, random, time
from dataclasses import dataclass
from .config import CONFIG, SensorPins

@dataclass
class SensorSnapshot:
    camera: str = "CONNECTED"
    gps: str = "CONNECTED"
    ai_engine: str = "ACTIVE"
    sensors: str = "ACTIVE"
    battery: int = 82
    storage: int = 68
    wifi: str = "CONNECTED"
    telegram: str = "READY"
    pir: str = "OK"
    ultrasonic: str = "OK"
    humidity_sensor: str = "OK"
    ir: str = "OK"
    gas: str = "OK"
    colour: str = "OK"
    touch: bool = False
    temp_c: float = 29.0
    humidity: float = 62.0
    distance_cm: float = 125.0
    aqi: int = 42
    smoke: str = "Low"
    lpg: str = "None"
    co2: str = "Normal"
    pulse_bpm: int = 76
    heart_status: str = "Normal"

class SensorHub:
    def __init__(self, pins: SensorPins = CONFIG.pins):
        self.pins = pins
        self.started = time.time()
        try:
            import RPi.GPIO as GPIO  # type: ignore
            self.GPIO = GPIO
            self.hardware = True
            GPIO.setmode(GPIO.BCM)
            for pin in [pins.gas_digital, pins.pir_data, pins.ir_data, pins.colour_out, pins.touch_sig]:
                GPIO.setup(pin, GPIO.IN)
            GPIO.setup(pins.ultrasonic_trig, GPIO.OUT)
            GPIO.setup(pins.ultrasonic_echo, GPIO.IN)
        except Exception:
            self.GPIO = None
            self.hardware = False

    def read(self) -> SensorSnapshot:
        t = time.time() - self.started
        snap = SensorSnapshot()
        snap.battery = max(15, int(82 - (t / 900) % 12))
        snap.storage = min(94, int(68 + (t / 1200) % 10))
        snap.temp_c = round(29 + math.sin(t / 18) * 1.6, 1)
        snap.humidity = round(62 + math.cos(t / 15) * 4.5, 1)
        snap.distance_cm = round(120 + math.sin(t / 7) * 45, 1)
        snap.aqi = max(18, min(165, int(42 + math.sin(t / 11) * 8)))
        snap.pulse_bpm = int(76 + math.sin(t * 1.7) * 5 + random.uniform(-1.5, 1.5))
        if self.hardware and self.GPIO:
            snap.touch = bool(self.GPIO.input(self.pins.touch_sig))
            snap.pir = "MOTION" if self.GPIO.input(self.pins.pir_data) else "OK"
            snap.ir = "OBJECT" if self.GPIO.input(self.pins.ir_data) else "OK"
            snap.gas = "ALERT" if self.GPIO.input(self.pins.gas_digital) else "OK"
            snap.colour = "ACTIVE" if self.GPIO.input(self.pins.colour_out) else "OK"
        else:
            snap.touch = int(t) % 17 in (0, 1, 2)
        return snap
