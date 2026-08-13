def pulse_report(snapshot):
    if snapshot.touch:
        return ["TOUCH DETECTED", "Person Name: Unknown", f"Heart Beat: {snapshot.pulse_bpm} BPM", f"Pulse: {snapshot.heart_status}", "Stress: Low", "Temperature: Normal"]
    return ["Touch sensor idle", "Place finger/palm on sensor", "Person Name: Unknown", "Heart Beat: --", "Pulse: Waiting"]
