"""Logger utility"""

import logging
import os


class Logger:
    """Logging utility for ScoreMorph-AI"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name):
        """
        Get or create a logger
        
        Args:
            name (str): Logger name
            
        Returns:
            logging.Logger: Logger instance
        """
        if name not in Logger._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            
            # Create logs directory if it doesn't exist
            log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # File handler
            file_handler = logging.FileHandler(
                os.path.join(log_dir, f'{name}.log')
            )
            file_handler.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
            Logger._loggers[name] = logger
        
        return Logger._loggers[name]
