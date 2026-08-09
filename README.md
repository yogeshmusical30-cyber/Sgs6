# Smart Guardian System (SGS) 2.0

A Raspberry Pi-ready neon dashboard for **SGS Visual**, developed by **M. Yogesh Naidu** and **Krishna Dev** at **NY Technologies**.

## Features

- Full-screen responsive Tkinter UI inspired by the SGS drone visual references.
- AirDroid phone camera feed from `http://192.168.0.100:4747/video` by default.
- Live OpenCV processing: humans are detected from the live feed and large blood-like regions are flagged only when they exceed noise thresholds.
- No fake permanent detection boxes; annotations are drawn only from live computer-vision results.
- Sensor dashboard for gas, PIR, DHT humidity, ultrasonic, IR, MPR121 wiring, colour sensor, and touch sensor.
- Startup voice line: “Welcome to SGS, developed by M. Yogesh Naidu and Krishna Dev. Admin mode.”
- Touch health panel with fluctuating pulse/heartbeat simulation when Raspberry Pi hardware is unavailable.
- Config placeholders for NVIDIA, map, and Telegram keys through environment variables.

## Hardware wiring

| Module | Pin |
| --- | --- |
| MQ gas AO | GPIO 19 |
| MQ gas DO | GPIO 13 |
| PIR data | GPIO 18 |
| DHT11/DHT22 data | GPIO 26 |
| Ultrasonic trig | GPIO 5 |
| Ultrasonic echo | GPIO 6 |
| IR data | GPIO 17 |
| MPR121 SCL | GPIO 23 |
| MPR121 SDA | GPIO 24 |
| Colour sensor OUT | GPIO 15 |
| Touch sensor SIG | GPIO 14 |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SGS_NVIDIA_API_KEY=""      # paste your key locally, never commit it
export SGS_MAP_API_KEY=""
export SGS_CAMERA_URL="http://192.168.0.100:4747/video"
python -m SGS.main
```

If you prefer routing AirDroid into `/dev/video0`, run this separately on the Raspberry Pi:

```bash
sudo ffmpeg -i http://192.168.0.100:4747/video -f v4l2 -pix_fmt yuv420p /dev/video0
```

## Safety note

SGS can assist with monitoring and first-aid guidance, but it is not a substitute for emergency services or professional medical care.
