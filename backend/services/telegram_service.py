import os
import requests

def _load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
    env_path = os.path.abspath(env_path)
    if not os.path.exists(env_path):
        return
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

_load_env()

TELEGRAM_TOKEN   = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def enviar_diagnostico(entrada):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print('[Telegram] Token o chat_id no configurados.')
        return

    sintomas_txt = ', '.join(entrada['sintomas'])
    top = entrada['diagnosticos'][0] if entrada['diagnosticos'] else None
    if not top:
        return

    mensaje = (
        f"🩺 *Doctor Byte - Diagnóstico #{entrada['id']}*\n"
        f"🕐 {entrada['fecha']}\n\n"
        f"*Síntomas:* {sintomas_txt}\n\n"
        f"*Diagnóstico principal:*\n"
        f"🔴 {top['nombre_falla']} ({top['porcentaje']}%)\n\n"
        f"*Recomendación:*\n{top['recomendacion']}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            'chat_id':    TELEGRAM_CHAT_ID,
            'text':       mensaje,
            'parse_mode': 'Markdown'
        }, timeout=5)
    except Exception as e:
        print(f'[Telegram] Error: {e}')