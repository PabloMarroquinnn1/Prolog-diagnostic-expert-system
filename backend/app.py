from flask import Flask
from flask_cors import CORS
from backend.routes.diagnose import diagnose_bp
from backend.routes.history_routes import history_bp
from backend.routes.crud_routes import crud_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(diagnose_bp, url_prefix='/api')
    app.register_blueprint(history_bp,  url_prefix='/api')
    app.register_blueprint(crud_bp, url_prefix='/api')

    @app.route('/api/health')
    def health():
        return {'ok': True, 'mensaje': 'Doctor Byte activo'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)