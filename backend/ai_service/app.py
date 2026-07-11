"""Main application entry point for ScoreMorph-AI backend"""

from flask import Flask, jsonify
from config import Config
from utils.logger import Logger


def create_app(config_class=Config):
    """
    Create and configure the Flask application
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize logger
    logger = Logger.get_logger(__name__)
    logger.info(f"Creating Flask app with {config_class.__name__} config")
    
    # Register blueprints
    try:
        from api.upload_routes import upload_bp
        from api.score_routes import score_bp
        from api.export_routes import export_bp
        
        app.register_blueprint(upload_bp)
        app.register_blueprint(score_bp)
        app.register_blueprint(export_bp)
        
        logger.info("All blueprints registered successfully")
    except ImportError as e:
        logger.error(f"Failed to import blueprints: {str(e)}")
        raise
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'environment': app.config.get('ENV', 'production')
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    logger.info("Flask app created successfully")
    return app


if __name__ == '__main__':
    import os
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Determine config class
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        from config import ProductionConfig
        config_class = ProductionConfig
    elif env == 'testing':
        from config import TestingConfig
        config_class = TestingConfig
    else:
        from config import DevelopmentConfig
        config_class = DevelopmentConfig
    
    # Create and run app
    app = create_app(config_class)
    
    # Get host and port from environment or use defaults
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = env == 'development'
    
    print(f"\n{'='*60}")
    print(f"🎵 ScoreMorph-AI Backend")
    print(f"{'='*60}")
    print(f"Starting Flask server...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Environment: {env}")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=debug)
