from flask import Blueprint

bp = Blueprint("calendar", __name__, url_prefix="/api/calendar")

@bp.route("/")
def calendar_stub():
    return {"message": "Calendar integration coming soon"}

