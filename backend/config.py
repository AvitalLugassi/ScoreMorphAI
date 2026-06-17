"""Configuration settings for ScoreMorph-AI backend"""

import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = False
    TESTING = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs', 'uploads')
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'ogg', 'm4a'}
    
    # Audio processing settings
    SAMPLE_RATE = 44100
    CHUNK_DURATION = 30  # seconds


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs', 'test_uploads')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
