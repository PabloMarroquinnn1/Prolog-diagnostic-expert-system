import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), '..', 'history.json')

def _load():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save(data):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def agregar_diagnostico(sintomas, diagnosticos):
    historial = _load()
    entrada = {
        'id':           len(historial) + 1,
        'fecha':        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sintomas':     sintomas,
        'diagnosticos': diagnosticos
    }
    historial.append(entrada)
    _save(historial)
    return entrada

def obtener_historial():
    return _load()

def limpiar_historial():
    _save([])