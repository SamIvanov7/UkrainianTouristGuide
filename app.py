from flask import Flask
from tourist_guide.routes import guide_bp

app = Flask(__name__)
app.register_blueprint(guide_bp)
