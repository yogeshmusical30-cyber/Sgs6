from .config import CONFIG

def send_alert(message: str, photo_path: str | None = None) -> bool:
    if not CONFIG.api.telegram_bot_token or not CONFIG.api.telegram_chat_id:
        return False
    # Integration point intentionally minimal; fill token/chat id through env vars.
    return False
