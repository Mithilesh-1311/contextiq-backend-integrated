from flask import Blueprint

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

@bp.route("/")
def tasks_stub():
    return {"message": "Tasks endpoint live"}

