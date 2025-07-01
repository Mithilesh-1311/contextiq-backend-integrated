
from flask import Blueprint, request, jsonify
from ..services import ai_tools

bp = Blueprint("ai", __name__, url_prefix="/api/ai")

@bp.route("/summarize", methods=["POST"])
def summarize_route():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    file_storage = request.files["file"]
    summary = ai_tools.summarise_file(file_storage)
    return jsonify({"summary": summary})

@bp.route("/flashcards", methods=["POST"])
def flashcards_route():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    file_storage = request.files["file"]
    cards = ai_tools.generate_flashcards(file_storage)
    return jsonify({"flashcards": cards})
