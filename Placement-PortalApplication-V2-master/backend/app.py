from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db, User
from models.student import Student
from models.company import Company
from models.drive import PlacementDrive
from models.application import Application

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from routes.student_routes import student_bp

import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)

    with app.app_context():
        db.create_all()
        initialize_admin()

    @app.route('/')
    def index():
        return {
            'success': True,
            'message': 'Placement Portal API',
            'version': '1.0.0'
        }

    @app.route('/health')
    def health():
        return {
            'status': 'healthy',
            'database': 'connected'
        }

    return app

def initialize_admin():
    admin_user = User.query.filter_by(email=Config.ADMIN_EMAIL).first()

    if not admin_user:
        admin_user = User(
            email=Config.ADMIN_EMAIL,
            role='admin',
            is_active=True
        )
        admin_user.set_password(Config.ADMIN_PASSWORD)

        try:
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user created: {Config.ADMIN_EMAIL}")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")
    else:
        print("Admin user already exists")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
