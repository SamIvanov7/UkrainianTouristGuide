from flask import Blueprint
from tourist_guide.routes import guide_bp

def register_blueprints(app):
    app.register_blueprint(guide_bp)

