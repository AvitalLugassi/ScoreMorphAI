"""Upload routes for handling audio file uploads"""

from flask import Blueprint, request, jsonify
from utils.file_manager import FileManager

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')


@upload_bp.route('/audio', methods=['POST'])
def upload_audio():
    """Handle audio file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    file_manager = FileManager()
    
    try:
        file_path = file_manager.save_upload(file)
        return jsonify({'success': True, 'file_path': file_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
