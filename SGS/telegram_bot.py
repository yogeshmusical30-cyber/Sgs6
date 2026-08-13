from __future__ import annotations

from typing import Optional
from .config import CONFIG


def send_alert(message: str, photo_path: Optional[str] = None) -> bool:
    """Send a Telegram alert when credentials are configured.

    The function returns False instead of crashing when requests, token, chat id,
    or network access are unavailable on the Raspberry Pi.
    """
    if not CONFIG.api.telegram_bot_token or not CONFIG.api.telegram_chat_id:
        return False
    try:
        import requests
        url = "https://api.telegram.org/bot{}/sendMessage".format(CONFIG.api.telegram_bot_token)
        response = requests.post(url, data={"chat_id": CONFIG.api.telegram_chat_id, "text": message}, timeout=8)
        return response.ok
    except Exception:
        return False
