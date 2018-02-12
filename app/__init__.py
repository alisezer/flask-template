# Flask Imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

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

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
