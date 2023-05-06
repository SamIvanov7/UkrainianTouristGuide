from tourist_guide import register_blueprints
from flask import Flask
def create_app():
    app = Flask(__name__)
    
    register_blueprints(app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
