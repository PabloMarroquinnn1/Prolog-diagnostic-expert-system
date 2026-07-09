from flask import Blueprint, jsonify
from backend.models.history import obtener_historial, limpiar_historial

history_bp = Blueprint('history', __name__)

@history_bp.route('/historial', methods=['GET'])
def get_historial():
    try:
        historial = obtener_historial()
        return jsonify({'ok': True, 'historial': historial})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@history_bp.route('/historial', methods=['DELETE'])
def delete_historial():
    try:
        limpiar_historial()
        return jsonify({'ok': True, 'mensaje': 'Historial limpiado'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500