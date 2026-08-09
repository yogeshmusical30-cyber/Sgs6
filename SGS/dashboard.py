from __future__ import annotations

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from .compat import optional_import
from .config import CONFIG
from .camera import CameraStream
from .sensors import SensorHub
from .logger import ActivityLogger
from .weather import current_weather
from .news import headlines
from .commands import COMMANDS, respond
from .pulse import pulse_report
from .maps import map_html
from .ai import ai_status

cv2 = optional_import("cv2")
Image = optional_import("PIL.Image")
ImageTk = optional_import("PIL.ImageTk")


class NeonDashboard(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(CONFIG.title)
        self.configure(bg="#020610")
        try:
            self.attributes("-fullscreen", True)
        except tk.TclError:
            self.geometry("1280x720")
        self.bind("<Escape>", lambda _event: self.attributes("-fullscreen", False))
        self.sensor = SensorHub()
        self.camera = CameraStream()
        self.log = ActivityLogger()
        self.camera.start()
        self._photo = None
        self._build()
        self.after(100, self._tick)

    def _panel(self, parent, title: str) -> tk.LabelFrame:
        return tk.LabelFrame(
            parent,
            text=title,
            fg="#39e8ff",
            bg="#06111d",
            bd=2,
            relief="ridge",
            font=("Playfair Display", 9, "bold"),
            labelanchor="nw",
        )

    def _text_panel(self, parent, title: str, width: int, height: int, fg: str = "white") -> tk.Text:
        panel = self._panel(parent, title)
        widget = tk.Text(panel, width=width, height=height, bg="#020912", fg=fg, insertbackground=fg, font=("Consolas", 8), relief="flat")
        widget.pack(fill="both", expand=True, padx=3, pady=3)
        panel.pack(fill="both", expand=True, pady=3)
        return widget

    def _build(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        header = tk.Frame(self, bg="#020610")
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=8, pady=4)
        tk.Label(header, text="SGS", fg="white", bg="#020610", font=("Playfair Display", 26, "bold")).pack(side="left")
        tk.Label(header, text="  SMART GUARDIAN SYSTEM", fg="#a7f6ff", bg="#020610", font=("Playfair Display", 10)).pack(side="left", anchor="s")
        tk.Label(header, text="{}\nLOCATION : {}".format(CONFIG.title, CONFIG.location_label), fg="#28dcff", bg="#020610", font=("Playfair Display", 20, "bold"), justify="center").pack(side="left", expand=True)
        self.date_lbl = tk.Label(header, fg="white", bg="#020610", font=("Consolas", 10), justify="left")
        self.date_lbl.pack(side="right")

        left = tk.Frame(self, bg="#020610")
        left.grid(row=1, column=0, sticky="ns", padx=6)
        center = tk.Frame(self, bg="#020610")
        center.grid(row=1, column=1, sticky="nsew")
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(0, weight=1)
        right = tk.Frame(self, bg="#020610")
        right.grid(row=1, column=2, sticky="ns", padx=6)
        bottom = tk.Frame(self, bg="#020610")
        bottom.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=5)

        self.status = self._text_panel(left, "SYSTEM STATUS", 24, 10, "#83ff4f")
        self.weather = self._text_panel(left, "WEATHER", 24, 7)
        self.news = self._text_panel(left, "NEWS HEADLINES", 24, 7)

        self.video = tk.Label(center, bg="#000", fg="#39e8ff", text="Waiting for AirDroid camera feed...", font=("Playfair Display", 18))
        self.video.grid(sticky="nsew")

        self.objects = self._text_panel(right, "OBJECTS DETECTED", 28, 6)
        self.analytics = self._text_panel(right, "AI ANALYTICS / COMMANDS", 28, 10, "#9cff6a")
        self.aqi = self._text_panel(right, "AIR QUALITY + TOUCH HEALTH", 28, 10, "#9cff6a")
        tk.Label(
            right,
            text="DEVELOPER INFO\nM. Yogesh Naidu + Krishna Dev\nBuilding For A Safer Tomorrow",
            fg="#39e8ff",
            bg="#06111d",
            font=("Playfair Display", 10, "bold"),
            justify="left",
        ).pack(fill="x", pady=4)

        self.command = self._bottom_text(bottom, "COMMAND CENTER", 35, "#83ff4f")
        self.info = self._bottom_text(bottom, "SYSTEM INFO", 30, "white")
        self.map = self._bottom_text(bottom, "LIVE MAP", 34, "#39e8ff")
        self.activity = self._bottom_text(bottom, "RECENT ACTIVITY LOG", 34, "white")
        chat_panel = self._panel(bottom, "CHAT SYSTEM")
        self.chat = tk.Text(chat_panel, width=35, height=5, bg="#020912", fg="white", font=("Consolas", 8), relief="flat")
        self.chat.pack(fill="both", expand=True)
        self.entry = ttk.Entry(chat_panel)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self._chat)
        chat_panel.pack(side="left", fill="both", expand=True, padx=3)

    def _bottom_text(self, parent, title: str, width: int, fg: str) -> tk.Text:
        panel = self._panel(parent, title)
        widget = tk.Text(panel, width=width, height=7, bg="#020912", fg=fg, font=("Consolas", 8), relief="flat")
        widget.pack(fill="both", expand=True)
        panel.pack(side="left", fill="both", expand=True, padx=3)
        return widget

    def _set(self, widget: tk.Text, text: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.configure(state="disabled")

    def _chat(self, _event) -> None:
        cmd = self.entry.get()
        self.entry.delete(0, "end")
        answer = respond(cmd)
        self.log.info("Command: {}".format(cmd))
        self.chat.insert("end", "YOU> {}\nSGS> {}\n".format(cmd, answer))

    def _show_frame(self, frame) -> None:
        if frame is None or cv2 is None or Image is None or ImageTk is None:
            return
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            view_width = max(640, self.video.winfo_width())
            view_height = max(360, self.video.winfo_height())
            image = Image.fromarray(rgb)
            image.thumbnail((view_width, view_height), Image.Resampling.LANCZOS)
            self._photo = ImageTk.PhotoImage(image)
            self.video.config(image=self._photo, text="")
        except Exception as exc:
            self.video.config(image="", text="Camera display error: {}".format(exc))

    def _tick(self) -> None:
        snap = self.sensor.read()
        frame, detections, camera_error = self.camera.latest()
        self.date_lbl.config(text="DATE : {:%d-%m-%Y}\nTIME : {:%I:%M:%S %p}\nMODE : NIGHT VISION AI".format(datetime.now(), datetime.now()))
        if frame is not None:
            self._show_frame(frame)
        elif camera_error:
            self.video.config(image="", text=camera_error)

        self._set(self.status, "\n".join([
            "● CAMERA        {}".format("CONNECTED" if not camera_error else "WAITING"),
            "● GPS           {}".format(snap.gps),
            "● AI ENGINE     {}".format(ai_status()),
            "● SENSORS       {}".format(snap.sensors),
            "● BATTERY       {}%".format(snap.battery),
            "● STORAGE       {}%".format(snap.storage),
            "● WIFI          {}".format(snap.wifi),
            "● TELEGRAM      {}".format(snap.telegram),
            "● PIR           {}".format(snap.pir),
            "● ULTRASONIC    {}".format(snap.ultrasonic),
            "● HUMIDITY      {}".format(snap.humidity_sensor),
            "● IR            {}".format(snap.ir),
            "● GAS           {}".format(snap.gas),
            "● COLOR SENSOR  {}".format(snap.colour),
            "● TOUCH SENSOR  {}".format("TOUCHED" if snap.touch else "IDLE"),
        ]))
        weather = current_weather()
        self._set(self.weather, "{}  {} {}\nHUMIDITY : {}%\nWIND     : {}\nVISIBILITY: {}\nTEMP     : {}°C".format(weather["icon"], weather["temperature"], weather["condition"], snap.humidity, weather["wind"], weather["visibility"], snap.temp_c))
        self._set(self.news, "\n".join("• " + headline for headline in headlines()))
        humans = sum(1 for detection in detections if detection.label == "HUMAN")
        blood = sum(1 for detection in detections if detection.label == "BLOOD")
        self._set(self.objects, "HUMANS   : {}\nVEHICLES : model optional\nOBJECTS  : live only\nBLOOD    : {}\nNo permanent fake boxes".format(humans, blood))
        self._set(self.analytics, "\n".join([
            "☑ No abnormal activity" if not blood else "⚠ Possible major bleeding",
            "☑ Traffic flow: normal",
            "☑ Pedestrians: safe",
            "☑ Environment: safe",
            "☑ Area status: secure",
            "",
        ] + COMMANDS))
        self._set(self.aqi, "AQI : {}\nAIR QUALITY : {}\nSMOKE : {}\nLPG : {}\nCO2 : {}\n\n{}".format(snap.aqi, "Good" if snap.aqi < 80 else "Moderate", snap.smoke, snap.lpg, snap.co2, "\n".join(pulse_report(snap))))
        self._set(self.command, "> SYSTEM ACTIVE AND MONITORING...\n> ALL SYSTEMS NORMAL\n> NO EMERGENCIES DETECTED\n> DATA LOGGING IN PROGRESS\n> STAY SAFE, STAY SECURE")
        self._set(self.info, "SYSTEM ID : {}\nGPS       : {}\nLOCATION  : {}\nMODE      : {}\nCAMERA    : AirDroid {}\nDEVS      : {}".format(CONFIG.system_id, CONFIG.gps_label, CONFIG.location_label, CONFIG.mode, CONFIG.camera_url, ", ".join(CONFIG.developers)))
        self._set(self.map, map_html(CONFIG.location_label))
        self._set(self.activity, "\n".join(self.log.latest()))
        self.after(100, self._tick)
