"""This is where we defined the Config files, which are used for initiating the
application with specific settings such as logger configurations or different
database setups."""

from app.utils.logging import file_logger, client_logger
from decouple import config as env_conf
import logging


class Config:
    # API configurations
    SECRET_KEY = env_conf("SECRET_KEY")
    # Database configurations
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class PostgreConfig(Config):
    # This configuration is used for setting up a postgre database. The
    # necessary settings are imported from the .env file.
    DB_USER = env_conf('DATABASE_USER')
    DB_PASSWORD = env_conf('DATABASE_PASS')
    DB_HOST = env_conf('DATABASE_HOST')
    DB_PORT = env_conf('DATABASE_PORT')
    DB_NAME = env_conf('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.\
        format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


class DockerPSQLConfig(PostgreConfig):
    # To initate the docker config. Basically adds bunch of logger handlers
    @classmethod
    def init_app(cls, app):
        PostgreConfig.init_app(app)
        # The default Flask logger level is set at ERROR, so if you want to see
        # INFO level or DEBUG level logs, you need to lower the main loggers
        # level first.
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(file_logger)
        app.logger.addHandler(client_logger)


# Create a config dictionary which is used while initiating the application.
# Config that is going to be used will be specified in the .env file
config_dict = {
    'postgre': PostgreConfig,
    'docker': DockerPSQLConfig,
}
