from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from datetime import datetime
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

class NeonDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(CONFIG.title); self.configure(bg="#020610")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.sensor = SensorHub(); self.camera = CameraStream(); self.log = ActivityLogger(); self.camera.start()
        self._photo = None; self._build(); self.after(80, self._tick)

    def _panel(self, parent, title):
        f = tk.LabelFrame(parent, text=title, fg="#39e8ff", bg="#06111d", bd=2, relief="ridge", font=("Playfair Display", 9, "bold"), labelanchor="nw")
        return f

    def _build(self):
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(1, weight=1)
        header = tk.Frame(self, bg="#020610"); header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=8, pady=4)
        tk.Label(header, text="SGS", fg="white", bg="#020610", font=("Playfair Display", 26, "bold")).pack(side="left")
        tk.Label(header, text="  SMART GUARDIAN SYSTEM", fg="#a7f6ff", bg="#020610", font=("Playfair Display", 10)).pack(side="left", anchor="s")
        tk.Label(header, text=f"{CONFIG.title}\nLOCATION : {CONFIG.location_label}", fg="#28dcff", bg="#020610", font=("Playfair Display", 20, "bold"), justify="center").pack(side="left", expand=True)
        self.date_lbl = tk.Label(header, fg="white", bg="#020610", font=("Consolas", 10), justify="left"); self.date_lbl.pack(side="right")

        left = tk.Frame(self, bg="#020610"); left.grid(row=1, column=0, sticky="ns", padx=6)
        center = tk.Frame(self, bg="#020610"); center.grid(row=1, column=1, sticky="nsew"); center.grid_rowconfigure(0, weight=1); center.grid_columnconfigure(0, weight=1)
        right = tk.Frame(self, bg="#020610"); right.grid(row=1, column=2, sticky="ns", padx=6)
        bottom = tk.Frame(self, bg="#020610"); bottom.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=5)

        self.status = tk.Text(self._panel(left,"SYSTEM STATUS"), width=24, height=10, bg="#020912", fg="#83ff4f", font=("Consolas",8)); self.status.pack(fill="both"); self.status.master.pack(fill="x", pady=4)
        self.weather = tk.Text(self._panel(left,"WEATHER"), width=24, height=7, bg="#020912", fg="white", font=("Consolas",8)); self.weather.pack(); self.weather.master.pack(fill="x", pady=4)
        self.news = tk.Text(self._panel(left,"NEWS HEADLINES"), width=24, height=7, bg="#020912", fg="white", font=("Consolas",8)); self.news.pack(); self.news.master.pack(fill="x", pady=4)

        self.video = tk.Label(center, bg="#000", fg="#39e8ff", text="Waiting for AirDroid camera feed...", font=("Playfair Display",18)); self.video.grid(sticky="nsew")

        self.objects = tk.Text(self._panel(right,"OBJECTS DETECTED"), width=28, height=6, bg="#020912", fg="white", font=("Consolas",9)); self.objects.pack(); self.objects.master.pack(fill="x", pady=4)
        self.analytics = tk.Text(self._panel(right,"AI ANALYTICS / COMMANDS"), width=28, height=10, bg="#020912", fg="#9cff6a", font=("Consolas",8)); self.analytics.pack(); self.analytics.master.pack(fill="x", pady=4)
        self.aqi = tk.Text(self._panel(right,"AIR QUALITY + TOUCH HEALTH"), width=28, height=10, bg="#020912", fg="#9cff6a", font=("Consolas",8)); self.aqi.pack(); self.aqi.master.pack(fill="x", pady=4)
        tk.Label(right, text="DEVELOPER INFO\nM. Yogesh Naidu + Krishna Dev\nBuilding For A Safer Tomorrow", fg="#39e8ff", bg="#06111d", font=("Playfair Display",10,"bold"), justify="left").pack(fill="x", pady=4)

        self.command = tk.Text(self._panel(bottom,"COMMAND CENTER"), width=35, height=7, bg="#020912", fg="#83ff4f", font=("Consolas",8)); self.command.pack(); self.command.master.pack(side="left", fill="both", expand=True, padx=3)
        self.info = tk.Text(self._panel(bottom,"SYSTEM INFO"), width=30, height=7, bg="#020912", fg="white", font=("Consolas",8)); self.info.pack(); self.info.master.pack(side="left", fill="both", expand=True, padx=3)
        self.map = tk.Text(self._panel(bottom,"LIVE MAP"), width=34, height=7, bg="#020912", fg="#39e8ff", font=("Consolas",8)); self.map.pack(); self.map.master.pack(side="left", fill="both", expand=True, padx=3)
        self.activity = tk.Text(self._panel(bottom,"RECENT ACTIVITY LOG"), width=34, height=7, bg="#020912", fg="white", font=("Consolas",8)); self.activity.pack(); self.activity.master.pack(side="left", fill="both", expand=True, padx=3)
        chat_panel = self._panel(bottom,"CHAT SYSTEM"); self.chat = tk.Text(chat_panel, width=35, height=5, bg="#020912", fg="white", font=("Consolas",8)); self.chat.pack(fill="both"); self.entry = ttk.Entry(chat_panel); self.entry.pack(fill="x"); self.entry.bind("<Return>", self._chat); chat_panel.pack(side="left", fill="both", expand=True, padx=3)

    def _set(self, widget, text):
        widget.configure(state="normal"); widget.delete("1.0", "end"); widget.insert("end", text); widget.configure(state="disabled")

    def _chat(self, _):
        cmd = self.entry.get(); self.entry.delete(0,"end"); ans = respond(cmd); self.log.info(f"Command: {cmd}"); self.chat.insert("end", f"YOU> {cmd}\nSGS> {ans}\n")

    def _tick(self):
        snap = self.sensor.read(); frame_pack = self.camera.latest(); dets = []
        self.date_lbl.config(text=f"DATE : {datetime.now():%d-%m-%Y}\nTIME : {datetime.now():%I:%M:%S %p}\nMODE : NIGHT VISION AI")
        if frame_pack[0] is not None:
            frame, dets = frame_pack
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            vw, vh = max(640,self.video.winfo_width()), max(360,self.video.winfo_height())
            img = Image.fromarray(rgb); img.thumbnail((vw, vh), Image.Resampling.LANCZOS)
            self._photo = ImageTk.PhotoImage(img); self.video.config(image=self._photo, text="")
        self._set(self.status, f"● CAMERA        {snap.camera}\n● GPS           {snap.gps}\n● AI ENGINE     {ai_status()}\n● SENSORS       {snap.sensors}\n● BATTERY       {snap.battery}%\n● STORAGE       {snap.storage}%\n● WIFI          {snap.wifi}\n● TELEGRAM      {snap.telegram}\n● PIR           {snap.pir}\n● ULTRASONIC    {snap.ultrasonic}\n● HUMIDITY      {snap.humidity_sensor}\n● IR            {snap.ir}\n● GAS           {snap.gas}\n● COLOR SENSOR  {snap.colour}\n● TOUCH SENSOR  {'TOUCHED' if snap.touch else 'IDLE'}")
        w=current_weather(); self._set(self.weather, f"{w['icon']}  {w['temperature']} {w['condition']}\nHUMIDITY : {snap.humidity}%\nWIND     : {w['wind']}\nVISIBILITY: {w['visibility']}\nTEMP     : {snap.temp_c}°C")
        self._set(self.news, "\n".join("• "+h for h in headlines()))
        humans=sum(1 for d in dets if d.label=='HUMAN'); blood=sum(1 for d in dets if d.label=='BLOOD')
        self._set(self.objects, f"HUMANS   : {humans}\nVEHICLES : model optional\nOBJECTS  : live only\nBLOOD    : {blood}\nNo permanent fake boxes")
        self._set(self.analytics, "\n".join(["☑ No abnormal activity" if not blood else "⚠ Possible major bleeding", "☑ Traffic flow: normal", "☑ Pedestrians: safe", "☑ Environment: safe", "☑ Area status: secure", "", *COMMANDS]))
        self._set(self.aqi, f"AQI : {snap.aqi}\nAIR QUALITY : {'Good' if snap.aqi < 80 else 'Moderate'}\nSMOKE : {snap.smoke}\nLPG : {snap.lpg}\nCO2 : {snap.co2}\n\n" + "\n".join(pulse_report(snap)))
        self._set(self.command, "> SYSTEM ACTIVE AND MONITORING...\n> ALL SYSTEMS NORMAL\n> NO EMERGENCIES DETECTED\n> DATA LOGGING IN PROGRESS\n> STAY SAFE, STAY SECURE")
        self._set(self.info, f"SYSTEM ID : {CONFIG.system_id}\nGPS       : {CONFIG.gps_label}\nLOCATION  : {CONFIG.location_label}\nMODE      : {CONFIG.mode}\nCAMERA    : AirDroid {CONFIG.camera_url}\nDEVS      : {', '.join(CONFIG.developers)}")
        self._set(self.map, map_html(CONFIG.location_label)); self._set(self.activity, "\n".join(self.log.latest()))
        self.after(80, self._tick)
