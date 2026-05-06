# app.py

from flask import Flask
from config import SECRET_KEY
from database.db import close_db

# Import blueprints
from routes.public import public_bp
from routes.admin import admin_bp
from routes.organiser import organiser_bp
from routes.agent import agent_bp
from routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    # ================================
    # CONFIG
    # ================================
    app.config['SECRET_KEY'] = SECRET_KEY

    # ================================
    # REGISTER BLUEPRINTS
    # ================================
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(organiser_bp, url_prefix='/organiser')
    app.register_blueprint(agent_bp, url_prefix='/agent')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # ================================
    # DB CONNECTION CLEANUP
    # ================================
    app.teardown_appcontext(close_db)

    # ================================
    # BASIC HEALTH ROUTE
    # ================================
    @app.route('/health')
    def health():
        return {"status": "running"}, 200

    return app


# ================================
# RUN APP
# ================================
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)