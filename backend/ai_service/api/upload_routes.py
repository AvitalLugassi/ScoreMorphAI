from flask import Blueprint, request, jsonify
from backend.utils.file_manager import FileManager
from backend.services.score_generator import generate
from backend.models.arrangement_request import ArrangementRequest

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')


@upload_bp.route('/audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    try:
        file_path = FileManager().save_upload(file)

        arrangement_request = ArrangementRequest(
            style=request.form.get('style', 'classical'),
            difficulty=request.form.get('difficulty', 'medium'),
            instruments=request.form.getlist('instruments') or ['piano'],
            voices_count=int(request.form.get('voices_count', 4))
        )

        result = generate(file_path, arrangement_request)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
