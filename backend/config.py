import os
class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    DEBUG = False
    TESTING = False

    # File upload settings

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__),
        'outputs',
        'uploads'
    )

    MAX_CONTENT_LENGTH = 500 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        'mp3',
        'wav',
        'flac',
        'ogg',
        'm4a'
    }

    # Audio settings

    SAMPLE_RATE = 44100
    CHUNK_DURATION = 30

    # Directories

    SEPARATED_DIR = "data/separated"
    MIDI_DIR = "data/midi"
    SCORE_DIR = "data/scores"

    # Demucs

    DEMUCS_MODEL = "htdemucs"

    # Output formats

    DEFAULT_MIDI_EXTENSION = ".mid"
    DEFAULT_XML_EXTENSION = ".musicxml"

    # Tempo

    DEFAULT_BPM = 120