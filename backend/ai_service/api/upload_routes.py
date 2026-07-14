import requests
from flask import Blueprint, request, jsonify
from utils.file_manager import FileManager
from services.music_processing_service import process_song
from models.arrangement_request import ArrangementRequest, Style, Difficulty, Instrument

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')


def _parse_request_params(form) -> ArrangementRequest:
    return ArrangementRequest(
        style=Style(form.get('style', 'classical')),
        difficulty=Difficulty(form.get('difficulty', 'medium')),
        instruments=[Instrument(i) for i in (form.getlist('instruments') or ['piano'])],
        voices_count=int(form.get('voices_count', 4))
    )


def _send_callback(callback_url: str, analysis):
    try:
        requests.put(callback_url, json={
            "midi_path":     analysis.arrangement_midi_path or analysis.melody_midi_path,
            "musicxml_path": analysis.arrangement_musicxml_path,
            "pdf_path":      analysis.pdf_path,
            "status":        "completed",
        }, timeout=10)
    except Exception:
        pass


@upload_bp.route('/audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    callback_url = request.form.get('callback_url')

    try:
        file_path = FileManager.save_upload(file)
        request_params = _parse_request_params(request.form)
        analysis = process_song(file_path, request_params)

        if callback_url:
            _send_callback(callback_url, analysis)

        return jsonify({
            "melody_midi_path":         analysis.melody_midi_path,
            "musicxml_path":            analysis.musicxml_path,
            "other_midi_path":          analysis.other_midi_path,
            "bass_midi_path":           analysis.bass_midi_path,
            "arrangement_midi_path":    analysis.arrangement_midi_path,
            "arrangement_musicxml_path": analysis.arrangement_musicxml_path,
            "pdf_path":                 analysis.pdf_path,
            "musical_key":              analysis.musical_key,
            "bpm":                      analysis.bpm,
            "style":                    request_params.style.value,
            "difficulty":               request_params.difficulty.value,
            "instruments":              [i.value for i in request_params.instruments],
            "voices_count":             request_params.voices_count,
        }), 200

    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
