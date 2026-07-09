from flask import Blueprint, request, jsonify
from backend.services.prolog_service import get_sintomas, diagnosticar
from backend.models.history import agregar_diagnostico
from backend.services.telegram_service import enviar_diagnostico

diagnose_bp = Blueprint('diagnose', __name__)

@diagnose_bp.route('/sintomas', methods=['GET'])
def listar_sintomas():
    try:
        sintomas = get_sintomas()
        return jsonify({'ok': True, 'sintomas': sintomas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@diagnose_bp.route('/sintomas/todos', methods=['GET'])
def listar_sintomas_todos():
    try:
        sintomas = get_sintomas()
        return jsonify({'ok': True, 'sintomas': sintomas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@diagnose_bp.route('/diagnosticar', methods=['POST'])
def hacer_diagnostico():
    try:
        body = request.get_json()
        sintomas = body.get('sintomas', [])
        if not sintomas:
            return jsonify({'ok': False, 'error': 'No se enviaron sintomas'}), 400
        diagnosticos = diagnosticar(sintomas)
        if not diagnosticos:
            return jsonify({'ok': True, 'diagnosticos': [], 'mensaje': 'No se encontraron fallas relacionadas'})
        entrada = agregar_diagnostico(sintomas, diagnosticos)
        enviar_diagnostico(entrada)
        return jsonify({'ok': True, 'diagnosticos': diagnosticos, 'id': entrada['id']})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500