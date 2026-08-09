from __future__ import annotations
import threading

def speak(text: str) -> None:
    def run():
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 155)
            engine.say(text)
            engine.runAndWait()
        except Exception:
            print(f"[VOICE] {text}")
    threading.Thread(target=run, daemon=True).start()
