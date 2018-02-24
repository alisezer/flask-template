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
    DB_USER = env_conf('DATABASE_USER')
    DB_PASSWORD = env_conf('DATABASE_PASS')
    DB_HOST = env_conf('DATABASE_HOST')
    DB_PORT = env_conf('DATABASE_PORT')
    DB_NAME = env_conf('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.\
        format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


class DockerPSQLConfig(PostgreConfig):
    @classmethod
    def init_app(cls, app):
        PostgreConfig.init_app(app)
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(file_logger)
        app.logger.addHandler(client_logger)


config_dict = {
    'docker': DockerPSQLConfig,
    # 'docker-sqlite': DockerSQLiteConfig
}


# TODO: marked for removal

# import os

# basedir = os.path.abspath(os.path.dirname(__file__))

# class SQLiteConfig(Config):
#     SQLALCHEMY_DATABASE_URI = \
#         'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# class DockerSQLiteConfig(SQLiteConfig):
#     @classmethod
#     def init_app(cls, app):
#         PostgreConfig.init_app(app)
#         app.logger.setLevel(logging.DEBUG)
#         app.logger.addHandler(file_logger)
#         app.logger.addHandler(client_logger)
