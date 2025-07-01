from flask import Blueprint, request, jsonify
from ..services import ai_tools

bp = Blueprint("notes_template", __name__, url_prefix="/api/notes-template")

@bp.route("/generate", methods=["POST"])
def generate_notes_template_route():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    file_storage = request.files["file"]
    template = ai_tools.generate_notes_template(file_storage)
    return jsonify({"template": template})
