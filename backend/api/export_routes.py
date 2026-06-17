"""Score generation routes"""

from flask import Blueprint, request, jsonify
from services.score_generator import ScoreGenerator

score_bp = Blueprint('score', __name__, url_prefix='/api/score')


@score_bp.route('/generate', methods=['POST'])
def generate_score():
    """Generate a score from audio file"""
    data = request.get_json()
    
    if not data or 'file_path' not in data:
        return jsonify({'error': 'No file path provided'}), 400
    
    try:
        generator = ScoreGenerator()
        score = generator.generate(data['file_path'])
        return jsonify({'success': True, 'score': score}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@score_bp.route('/list', methods=['GET'])
def list_scores():
    """List all generated scores"""
    # Implementation here
    return jsonify({'scores': []}), 200
