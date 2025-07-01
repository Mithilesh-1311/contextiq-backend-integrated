from flask import Flask
from app.extensions import db, jwt, cors, api, configure_logger
from app.config import settings
from app.blueprints import auth, tasks, notes, calendar, ai, plan, notes_template

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
        RESTX_MASK_SWAGGER=False,
        ERROR_404_HELP=False,
    )
    configure_logger(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    api.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(calendar.bp)
    app.register_blueprint(plan.bp)
    app.register_blueprint(notes_template.bp)

    return app
