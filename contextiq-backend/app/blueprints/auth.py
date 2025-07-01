from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.route("/")
def login_stub():
    return {"message": "Auth blueprint is active"}

