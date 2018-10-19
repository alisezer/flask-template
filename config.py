"""This is where we defined the Config files, which are used for initiating the
application with specific settings such as logger configurations or different
database setups."""

from app.utils.logging import file_logger, client_logger
from decouple import config as env_conf
import logging


class LocalPSQLConfig:
    # To initate the local config. Basically adds bunch of logger handlers with
    # a postgre sql setup

    DB_USER = env_conf('DATABASE_USER')
    DB_PASSWORD = env_conf('DATABASE_PASS')
    DB_HOST = env_conf('DATABASE_HOST')
    DB_PORT = env_conf('DATABASE_PORT')
    DB_NAME = env_conf('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.\
        format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    SECRET_KEY = env_conf("SECRET_KEY", cast=str, default="12345")

    @classmethod
    def init_app(cls, app):
        # The default Flask logger level is set at ERROR, so if you want to see
        # INFO level or DEBUG level logs, you need to lower the main loggers
        # level first.
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(file_logger)
        app.logger.addHandler(client_logger)


class Develop:
    """Development config geared towards docker."""
    # Database configurations
    DB_USER = "deploy"
    DB_PASSWORD = "docker"
    DB_HOST = "db"
    DB_PORT = "5432"
    DB_NAME = "stories"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # DEBUG = True
    # API configurations
    SECRET_KEY = env_conf("SECRET_KEY", cast=str, default="12345")

    @staticmethod
    def init_app(app):
        """Initiates application."""
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(client_logger)
        app.logger.addHandler(file_logger)


# Create a config dictionary which is used while initiating the application.
# Config that is going to be used will be specified in the .env file
config_dict = {
    'localpsql': LocalPSQLConfig,
    'develop': Develop,
}
