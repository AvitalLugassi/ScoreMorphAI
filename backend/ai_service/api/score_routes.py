from flask import Blueprint, request, jsonify
from services.music_processing_service import process_song
from models.arrangement_request import ArrangementRequest, Style, Difficulty, Instrument

score_bp = Blueprint('score', __name__, url_prefix='/api/score')


@score_bp.route('/generate', methods=['POST'])
def generate_score():
    """Generate a score from an already-uploaded audio file path."""
    data = request.get_json()

    if not data or 'file_path' not in data:
        return jsonify({'error': 'No file path provided'}), 400

    try:
        request_params = ArrangementRequest(
            style=Style(data.get('style', 'classical')),
            difficulty=Difficulty(data.get('difficulty', 'medium')),
            instruments=[Instrument(i) for i in data.get('instruments', ['piano'])],
            voices_count=data.get('voices_count', 4)
        )

        analysis = process_song(data['file_path'], request_params)

        return jsonify({
            "melody_midi_path": analysis.melody_midi_path,
            "musicxml_path": analysis.musicxml_path,
            "other_midi_path": analysis.other_midi_path,
            "bass_midi_path": analysis.bass_midi_path,
            "arrangement_midi_path": analysis.arrangement_midi_path,
            "arrangement_musicxml_path": analysis.arrangement_musicxml_path,
            "pdf_path": analysis.pdf_path,
            "musical_key": analysis.musical_key,
            "bpm": analysis.bpm,
            "style": request_params.style.value,
            "difficulty": request_params.difficulty.value,
            "instruments": [i.value for i in request_params.instruments],
            "voices_count": request_params.voices_count
        }), 200

    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
