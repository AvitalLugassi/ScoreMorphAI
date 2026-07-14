from flask import Blueprint, request, jsonify, send_file
import os

export_bp = Blueprint('export', __name__, url_prefix='/api/export')


@export_bp.route('/pdf', methods=['GET'])
def export_pdf():
    """Download a generated PDF score by path."""
    pdf_path = request.args.get('path')
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF not found'}), 404
    return send_file(pdf_path, as_attachment=True, download_name='arrangement.pdf')


@export_bp.route('/musicxml', methods=['GET'])
def export_musicxml():
    """Download a generated MusicXML file by path."""
    xml_path = request.args.get('path')
    if not xml_path or not os.path.exists(xml_path):
        return jsonify({'error': 'MusicXML not found'}), 404
    return send_file(xml_path, as_attachment=True, download_name='arrangement.musicxml')


@export_bp.route('/midi', methods=['GET'])
def export_midi():
    """Download a generated MIDI file by path."""
    midi_path = request.args.get('path')
    if not midi_path or not os.path.exists(midi_path):
        return jsonify({'error': 'MIDI not found'}), 404
    return send_file(midi_path, as_attachment=True, download_name='arrangement.mid')
