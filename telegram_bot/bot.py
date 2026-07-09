import os
import time
import requests

def _load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    env_path = os.path.abspath(env_path)
    if not os.path.exists(env_path):
        return
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

TOKEN        = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID      = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:5000/api')

print(f"TOKEN: {TOKEN}")

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}/sendMessage", json={
        "chat_id": chat_id,
        "text":    text,
        "parse_mode": "Markdown"
    }, timeout=10)


def get_updates(offset=None):
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    res = requests.get(f"{TELEGRAM_API}/getUpdates",
                       params=params, timeout=35)
    data = res.json()
    print(f"Updates: {data}")
    return data


def get_sintomas():
    res = requests.get(f"{BACKEND_URL}/sintomas/todos", timeout=10)
    return res.json().get("sintomas", [])


def diagnosticar(sintomas):
    res = requests.post(f"{BACKEND_URL}/diagnosticar",
                        json={"sintomas": sintomas}, timeout=15)
    return res.json()


def get_historial():
    res = requests.get(f"{BACKEND_URL}/historial", timeout=10)
    return res.json().get("historial", [])


# ── Estado de conversación por usuario ───────────────────────
sesiones = {}


def handle_update(update):
    message = update.get("message")
    if not message:
        return

    chat_id  = str(message["chat"]["id"])
    text     = message.get("text", "").strip()
    username = message.get("from", {}).get("username") or \
               message.get("from", {}).get("first_name", "Usuario")

    if chat_id not in sesiones:
        sesiones[chat_id] = {"estado": "idle", "sintomas": []}

    sesion = sesiones[chat_id]

    # ── Comandos ──────────────────────────────────────────────
    if text == "/start":
        sesion["estado"]   = "idle"
        sesion["sintomas"] = []
        send_message(chat_id,
            f"👋 Hola *{username}*, bienvenido a *Doctor Byte*\n\n"
            "Sistema experto de diagnóstico de fallas en computadoras.\n\n"
            "Comandos disponibles:\n"
            "/diagnosticar - Iniciar diagnóstico\n"
            "/historial    - Ver últimos diagnósticos\n"
            "/sintomas     - Ver síntomas disponibles\n"
            "/cancelar     - Cancelar operación actual"
        )
        return

    if text == "/cancelar":
        sesion["estado"]   = "idle"
        sesion["sintomas"] = []
        send_message(chat_id, "❌ Operación cancelada.")
        return

    if text == "/sintomas":
        sintomas = get_sintomas()
        if not sintomas:
            send_message(chat_id, "No se pudieron cargar los síntomas.")
            return
        msg = "📋 *Síntomas disponibles:*\n\n"
        for i, s in enumerate(sintomas, 1):
            msg += f"{i}. {s['nombre']} (`{s['id']}`)\n"
        send_message(chat_id, msg)
        return

    if text == "/historial":
        historial = get_historial()
        if not historial:
            send_message(chat_id, "No hay diagnósticos en el historial.")
            return
        msg = "📂 *Últimos diagnósticos:*\n\n"
        for h in historial[-5:][::-1]:
            top = h["diagnosticos"][0] if h["diagnosticos"] else None
            if top:
                msg += (f"🔹 #{h['id']} · {h['fecha']}\n"
                        f"   {top['nombre_falla']} ({top['porcentaje']}%)\n\n")
        send_message(chat_id, msg)
        return

    if text == "/diagnosticar":
        sesion["estado"]   = "eligiendo_sintomas"
        sesion["sintomas"] = []
        sintomas = get_sintomas()
        msg = (
            "🩺 *Modo diagnóstico activado*\n\n"
            "Escribe los IDs de los síntomas uno por uno.\n"
            "Cuando termines escribe /listo\n\n"
            "*Síntomas disponibles:*\n"
        )
        for s in sintomas:
            msg += f"• `{s['id']}` — {s['nombre']}\n"
        send_message(chat_id, msg)
        return

    if text == "/listo":
        if sesion["estado"] != "eligiendo_sintomas":
            send_message(chat_id, "Primero inicia un diagnóstico con /diagnosticar")
            return
        if not sesion["sintomas"]:
            send_message(chat_id, "No agregaste ningún síntoma. Usa /diagnosticar para empezar.")
            return

        send_message(chat_id, "⏳ Analizando síntomas...")
        data = diagnosticar(sesion["sintomas"])
        diagnosticos = data.get("diagnosticos", [])

        if not diagnosticos:
            send_message(chat_id, "No se encontraron fallas relacionadas.")
        else:
            msg = "🔍 *Resultados del diagnóstico:*\n\n"
            for d in diagnosticos[:3]:
                barra = "█" * (d["porcentaje"] // 10) + "░" * (10 - d["porcentaje"] // 10)
                msg += (
                    f"*{d['nombre_falla']}*\n"
                    f"`{barra}` {d['porcentaje']}%\n"
                    f"💡 {d['recomendacion']}\n\n"
                )
            send_message(chat_id, msg)

        sesion["estado"]   = "idle"
        sesion["sintomas"] = []
        return

    # ── Modo eligiendo síntomas ───────────────────────────────
    if sesion["estado"] == "eligiendo_sintomas":
        sid = text.lower().replace(" ", "_")
        if sid in sesion["sintomas"]:
            send_message(chat_id, f"⚠️ `{sid}` ya fue agregado.")
        else:
            sesion["sintomas"].append(sid)
            send_message(chat_id,
                f"✅ Agregado: `{sid}`\n"
                f"Total: {len(sesion['sintomas'])} síntoma(s)\n"
                f"Escribe otro o /listo para diagnosticar."
            )
        return

    send_message(chat_id,
        "No entendí ese comando.\n"
        "Usa /start para ver los comandos disponibles."
    )


def main():
    print("Doctor Byte Bot iniciado...")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                handle_update(update)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()