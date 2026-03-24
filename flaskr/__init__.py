import os
from flask import Flask, app
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_cors import CORS
from .config import config

mongo = PyMongo()
jwt = JWTManager()
cors = CORS()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Determine config name (default to 'development' if not provided)
    config_name = test_config if isinstance(test_config, str) else 'development'
    app_config = config.get(config_name, config['development'])
    app.config.from_object(app_config)

    print("Config loaded from object:", app_config)
    print("MONGO_URI in app.config:", app.config.get('MONGO_URI'))

    # If test_config is a dict, override config values (for testing)
    if isinstance(test_config, dict):
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    print("MONGO_URI:", app.config.get('MONGO_URI'))
    print("MONGO_DBNAME:", app.config.get('MONGO_DBNAME'))  # if you kept it

    mongo.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    print("mongo.db after init:", mongo.db)
    print("mongo.cx after init:", mongo.cx)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    from .routes.accounts import accounts_bp
    app.register_blueprint(accounts_bp, url_prefix='/api/accounts')

    from .routes.transactions import transactions_bp
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')

    @app.route('/health')
    def health_check():
        try:
            # If mongo.db is None, get the database from the client
            if mongo.db is None:
                db = mongo.cx.get_database("banking_db")   # or use the name from config
                db.command('ping')
            else:
                mongo.db.command('ping')
            return {"status": "ok", "database": "connected"}
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

    return app