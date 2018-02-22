from flask_migrate import Migrate, upgrade
from app import create_app, db
from decouple import config

env_config = config('ENV', cast=str)

app = create_app(env_config)
migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """Run deployment tasks"""
    # Migrate database to latest revision
    upgrade()
