from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS
import logging
from colorlog import ColoredFormatter

db = SQLAlchemy()
jwt = JWTManager()
api = Api(title="ContextIQ API", version="1.0", doc="/docs")
cors = CORS(resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

def configure_logger(app):
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(asctime)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    ))
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
