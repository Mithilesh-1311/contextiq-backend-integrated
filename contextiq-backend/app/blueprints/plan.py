from flask import Blueprint, jsonify
from app.services import planner

bp = Blueprint("plan", __name__, url_prefix="/api/plan")

@bp.route("/suggest", methods=["GET"])
def suggest_plan_route():
    return jsonify(planner.suggest_plan())
