import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Determine config name (default to 'development' if not provided)
    config_name = test_config if isinstance(test_config, str) else 'development'
    app_config = config.get(config_name, config['development'])
    app.config.from_object(app_config)

    # If test_config is a dict, override config values (for testing)
    if isinstance(test_config, dict):
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app