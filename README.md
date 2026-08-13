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
- Compatible with both `python -m SGS.main` and `python SGS/main.py` launch styles.

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
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SGS_NVIDIA_API_KEY=""      # paste your key locally, never commit it
export SGS_MAP_API_KEY=""
export SGS_CAMERA_URL="http://192.168.0.100:4747/video"
python -m SGS.main
```

You can also run this from the repository root:

```bash
python SGS/main.py
```

If `opencv-python` is slow or fails to build on Raspberry Pi, use the system package instead:

```bash
sudo apt update
sudo apt install -y python3-opencv python3-pil python3-tk espeak ffmpeg
```

If you prefer routing AirDroid into `/dev/video0`, run this separately on the Raspberry Pi:

```bash
sudo ffmpeg -i http://192.168.0.100:4747/video -f v4l2 -pix_fmt yuv420p /dev/video0
```

## Troubleshooting

- If the dashboard says it is waiting for AirDroid, open `http://192.168.0.100:4747/video` in a browser on the Raspberry Pi first and confirm the phone and Pi are on the same Wi-Fi.
- If there is no desktop display, run from the Raspberry Pi GUI terminal, not a pure SSH terminal, or set `DISPLAY=:0`.
- If voice does not speak, install `espeak` and keep `pyttsx3` installed in the active Python environment.
- If GPIO is unavailable on a laptop, SGS runs in safe simulation mode instead of crashing.

## Safety note

SGS can assist with monitoring and first-aid guidance, but it is not a substitute for emergency services or professional medical care.
