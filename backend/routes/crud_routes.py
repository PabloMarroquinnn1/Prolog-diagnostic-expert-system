from flask import Blueprint, request, jsonify
from backend.services.prolog_crud_service import (
    crear_sintoma, eliminar_sintoma, listar_sintomas_dynamic,
    crear_falla, eliminar_falla, listar_fallas_dynamic, actualizar_falla,
    crear_recomendacion, actualizar_recomendacion, eliminar_recomendacion, listar_recomendaciones_dynamic,
    listar_reglas, crear_regla, eliminar_regla
)
from backend.services.bot_config_service import (
    get_bot_config, update_bot_config, toggle_bot
)

crud_bp = Blueprint('crud', __name__)

# ── Síntomas ──────────────────────────────────────────────────

@crud_bp.route('/crud/sintomas', methods=['GET'])
def get_sintomas_dynamic():
    return jsonify({'ok': True, 'sintomas': listar_sintomas_dynamic()})

@crud_bp.route('/crud/sintomas', methods=['POST'])
def post_sintoma():
    body = request.get_json()
    sid    = body.get('id', '').strip().replace(' ', '_')
    nombre = body.get('nombre', '').strip()
    if not sid or not nombre:
        return jsonify({'ok': False, 'error': 'id y nombre son requeridos'}), 400
    ok, msg = crear_sintoma(sid, nombre)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 409)

@crud_bp.route('/crud/sintomas/<sid>', methods=['DELETE'])
def delete_sintoma(sid):
    ok, msg = eliminar_sintoma(sid)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 404)

# ── Fallas ────────────────────────────────────────────────────

@crud_bp.route('/crud/fallas', methods=['GET'])
def get_fallas_dynamic():
    return jsonify({'ok': True, 'fallas': listar_fallas_dynamic()})

@crud_bp.route('/crud/fallas', methods=['POST'])
def post_falla():
    body          = request.get_json()
    fid           = body.get('id', '').strip().replace(' ', '_')
    nombre        = body.get('nombre', '').strip()
    sintomas      = body.get('sintomas', [])
    recomendacion = body.get('recomendacion', '').strip()
    if not fid or not nombre or not sintomas or not recomendacion:
        return jsonify({'ok': False, 'error': 'Todos los campos son requeridos'}), 400
    ok, msg = crear_falla(fid, nombre, sintomas, recomendacion)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 409)

@crud_bp.route('/crud/fallas/<fid>', methods=['PUT'])
def put_falla(fid):
    body          = request.get_json()
    nombre        = body.get('nombre', '').strip()
    sintomas      = body.get('sintomas', [])
    recomendacion = body.get('recomendacion', '').strip()
    ok, msg = actualizar_falla(fid, nombre, sintomas, recomendacion)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 404)

@crud_bp.route('/crud/fallas/<fid>', methods=['DELETE'])
def delete_falla(fid):
    ok, msg = eliminar_falla(fid)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 404)

# ── Recomendaciones ───────────────────────────────────────────

@crud_bp.route('/crud/recomendaciones', methods=['GET'])
def get_recomendaciones():
    return jsonify({'ok': True, 'recomendaciones': listar_recomendaciones_dynamic()})

@crud_bp.route('/crud/recomendaciones', methods=['POST'])
def post_recomendacion():
    body  = request.get_json()
    fid   = body.get('falla_id', '').strip()
    texto = body.get('texto', '').strip()
    if not fid or not texto:
        return jsonify({'ok': False, 'error': 'falla_id y texto son requeridos'}), 400
    ok, msg = crear_recomendacion(fid, texto)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 409)

@crud_bp.route('/crud/recomendaciones/<fid>', methods=['PUT'])
def put_recomendacion(fid):
    body  = request.get_json()
    texto = body.get('texto', '').strip()
    ok, msg = actualizar_recomendacion(fid, texto)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 404)

@crud_bp.route('/crud/recomendaciones/<fid>', methods=['DELETE'])
def delete_recomendacion(fid):
    ok, msg = eliminar_recomendacion(fid)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 404)

# ── Reglas ────────────────────────────────────────────────────

@crud_bp.route('/crud/reglas', methods=['GET'])
def get_reglas():
    return jsonify({'ok': True, 'reglas': listar_reglas()})

@crud_bp.route('/crud/reglas', methods=['POST'])
def post_regla():
    body     = request.get_json()
    fid      = body.get('falla_id', '').strip().replace(' ', '_')
    sintomas = body.get('sintomas', [])
    if not fid or not sintomas:
        return jsonify({'ok': False, 'error': 'falla_id y sintomas son requeridos'}), 400
    ok, msg = crear_regla(fid, sintomas)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 409)

@crud_bp.route('/crud/reglas/<fid>', methods=['DELETE'])
def delete_regla(fid):
    ok, msg = eliminar_regla(fid)
    return jsonify({'ok': ok, 'mensaje': msg}), (200 if ok else 404)

# ── Bot config ────────────────────────────────────────────────

@crud_bp.route('/crud/bot/config', methods=['GET'])
def get_config():
    return jsonify({'ok': True, 'config': get_bot_config()})

@crud_bp.route('/crud/bot/config', methods=['PUT'])
def put_config():
    body = request.get_json()
    update_bot_config(body)
    return jsonify({'ok': True, 'mensaje': 'Configuracion actualizada'})

@crud_bp.route('/crud/bot/toggle', methods=['POST'])
def post_toggle():
    activo = toggle_bot()
    return jsonify({'ok': True, 'activo': activo})