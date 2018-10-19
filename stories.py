"""This file is the main module which contains the app, where all the good
stuff happens. You will always want to point your applications like Gunicorn
to this file, which will pick up the app to run their servers.
"""
from flask_migrate import Migrate, upgrade
from app import create_app, db
from decouple import config

# Config to be used is read from the .env file, and then used for initiaing the
# application with the preconfigured create_app method.
env_config = config("ENV", cast=str, default="develop")

app = create_app(env_config)
migrate = Migrate(app, db)

# More custom commands can be added to flasks CLI here(for running tests and
# other stuff)


@app.cli.command()
def deploy():
    """Run deployment tasks"""
    # Migrate database to latest revision
    upgrade()
