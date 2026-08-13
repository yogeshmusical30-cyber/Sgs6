COMMANDS = ["Hello SGS", "Scan wound", "Check pulse", "Start camera", "Stop camera", "Emergency mode", "Gas leak", "Call ambulance", "Call police", "Fire emergency", "Medical emergency", "CPR help", "Sensor status", "Admin mode"]

def respond(command: str) -> str:
    c = command.lower().strip()
    if "pulse" in c: return "Pulse scan ready. Touch sensor enabled; reading will fluctuate live."
    if "wound" in c: return "Wound scanner active. Only large red regions are treated as possible bleeding."
    if "gas" in c: return "Gas protocol active. Ventilate area and avoid sparks if gas is detected."
    if "help" in c or "cpr" in c: return "Call emergency services. Start CPR only if trained and the person is unresponsive and not breathing normally."
    return "SGS command received. Monitoring health, hygiene, safety, sensors, camera, and alerts."
