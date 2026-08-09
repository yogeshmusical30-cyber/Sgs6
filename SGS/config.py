"""Configuration for Smart Guardian System (SGS)."""
from __future__ import annotations

from dataclasses import dataclass, field
import os


@dataclass(frozen=True)
class SensorPins:
    gas_analog: int = 19
    gas_digital: int = 13
    pir_data: int = 18
    humidity_data: int = 26
    ultrasonic_trig: int = 5
    ultrasonic_echo: int = 6
    ir_data: int = 17
    mpr121_scl: int = 23
    mpr121_sda: int = 24
    colour_out: int = 15
    touch_sig: int = 14


@dataclass(frozen=True)
class ApiConfig:
    # Put secrets in environment variables. Do not hard-code API keys in source.
    nvidia_api_key: str = field(default_factory=lambda: os.getenv("SGS_NVIDIA_API_KEY", ""))
    map_api_key: str = field(default_factory=lambda: os.getenv("SGS_MAP_API_KEY", ""))
    telegram_bot_token: str = field(default_factory=lambda: os.getenv("SGS_TELEGRAM_BOT_TOKEN", ""))
    telegram_chat_id: str = field(default_factory=lambda: os.getenv("SGS_TELEGRAM_CHAT_ID", ""))


@dataclass(frozen=True)
class AppConfig:
    title: str = "SGS VISUAL"
    system_name: str = "Smart Guardian System 2.0"
    system_id: str = "SGS-KVDRDO-001"
    location_label: str = "KVDRDO BLR"
    gps_label: str = "13.0103° N, 77.6535° E"
    mode: str = "ADMIN MODE"
    camera_url: str = field(default_factory=lambda: os.getenv("SGS_CAMERA_URL", "http://192.168.0.100:4747/video"))
    developers: tuple[str, ...] = ("M. Yogesh Naidu", "Krishna Dev")
    company: str = "NY Technologies"
    pins: SensorPins = field(default_factory=SensorPins)
    api: ApiConfig = field(default_factory=ApiConfig)


CONFIG = AppConfig()
