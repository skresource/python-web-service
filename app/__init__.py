from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app(config_class=Config):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    print(f"###### Application started......")
    if app.config.get("OPENAI_API_KEY") !="":
        print("\033[92m#### OPENAI_API_KEY is set ####\033[0m")
    else:
        print("\033[91mOPENAI_API_KEY is not set\033[0m")
     
     
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    # Register blueprints
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


# Unable to see the login screen. No error showing. Steps to reproduce, launch the 
# application then click on sign in. Blank page loaded.