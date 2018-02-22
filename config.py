from app.utils.logging import file_logger, client_logger
from decouple import config as env_conf
import logging
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # API configurations
    SECRET_KEY = env_conf("SECRET_KEY")ftemplate

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


# class SQLiteConfig(Config):
#     SQLALCHEMY_DATABASE_URI = env_conf('DEV_DATABASE_URL') or \
#             'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class DockerConfig(PostgreConfig):
    @classmethod
    def init_app(cls, app):
        PostgreConfig.init_app(app)
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(file_logger)
        app.logger.addHandler(client_logger)


config_dict = {
    'docker': DockerConfig
}
