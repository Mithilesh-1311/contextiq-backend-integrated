from flask import Blueprint

bp = Blueprint("notes", __name__, url_prefix="/api/notes")

@bp.route("/")
def notes_stub():
    return {"message": "Notes service here"}

