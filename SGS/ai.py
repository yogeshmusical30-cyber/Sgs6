from .config import CONFIG

def ai_status():
    return "NVIDIA API READY" if CONFIG.api.nvidia_api_key else "LOCAL AI MODE"
