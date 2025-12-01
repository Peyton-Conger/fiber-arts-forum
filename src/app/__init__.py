from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config as _C

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(_C)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        # register blueprints
        from .auth import auth_bp
        from .forum import forum_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(forum_bp, url_prefix='/')\n        from .api import api_bp\n        app.register_blueprint(api_bp)

        # create db for dev
        from pathlib import Path
        Path('instance').mkdir(exist_ok=True)
        Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
        db.create_all()

    return app
