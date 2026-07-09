import os
import json

CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'bot_config.json')
)

DEFAULT_CONFIG = {
    'activo':           True,
    'token':            os.getenv('TELEGRAM_TOKEN', ''),
    'chat_id':          os.getenv('TELEGRAM_CHAT_ID', ''),
    'msg_bienvenida':   'Bienvenido a Doctor Byte. Sistema experto de diagnostico de fallas.',
    'msg_no_resultado': 'No encontre fallas relacionadas con esos sintomas.',
    'msg_error':        'Ocurrio un error. Intenta de nuevo.'
}

def _load():
    if not os.path.exists(CONFIG_PATH):
        _save(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save(data):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_bot_config():
    return _load()

def update_bot_config(nuevos_valores):
    config = _load()
    config.update(nuevos_valores)
    _save(config)

def toggle_bot():
    config = _load()
    config['activo'] = not config['activo']
    _save(config)
    return config['activo']