from decouple import config as env_conf
import os


class Config(object):
    # Database configurations
    DB_USER = env_conf('DATABASE_USER')
    DB_PASSWORD = env_conf('DATABASE_HOST')
    DB_HOST = env_conf('DATABASE_HOST')
    DB_PORT = env_conf('DATABASE_PORT')
    DB_NAME = env_conf('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.\
        format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # DEBUG = True

    # API configurations
    SECRET_KEY = env_conf("SECRET_KEY")
