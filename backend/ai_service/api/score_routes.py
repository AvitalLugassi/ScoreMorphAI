"""Export routes for downloading generated scores"""

from flask import Blueprint, request, jsonify, send_file
from services.export_service import ExportService

export_bp = Blueprint('export', __name__, url_prefix='/api/export')


@export_bp.route('/score/<score_id>', methods=['GET'])
def export_score(score_id):
    """Export a score in specified format"""
    export_format = request.args.get('format', 'pdf')
    
    try:
        exporter = ExportService()
        file_path = exporter.export(score_id, export_format)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@export_bp.route('/score/<score_id>/formats', methods=['GET'])
def get_available_formats(score_id):
    """Get available export formats for a score"""
    formats = ['pdf', 'musicxml', 'midi', 'png']
    return jsonify({'formats': formats}), 200
