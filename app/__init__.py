# Flask Imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

# Internal 
from app.main import main as main_blueprint
from app.api import api as api_blueprint

# Other
from config import Config

# Setup
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Logger configs
    # app.logger.addHandler(file_logger)
    # app.logger.addHandler(client_logger)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
