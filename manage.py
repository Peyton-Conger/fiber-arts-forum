from flask import current_app
from flask_migrate import Migrate, MigrateCommand
from flask.cli import FlaskGroup
from src.app import create_app, db
from src.app import models

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    cli()
