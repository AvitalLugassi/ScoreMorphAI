"""File manager utility"""

import os
from werkzeug.utils import secure_filename
from config import Config


class FileManager:
    """Utility for managing file operations"""
    
    ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
    UPLOAD_FOLDER = Config.UPLOAD_FOLDER
    
    @staticmethod
    def allowed_file(filename):
        """Check if file has allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FileManager.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_upload(file):
        """
        Save uploaded file
        
        Args:
            file: File object from request
            
        Returns:
            str: Path to saved file
        """
        if not file or file.filename == '':
            raise ValueError('No file selected')
        
        if not FileManager.allowed_file(file.filename):
            raise ValueError(f'File type not allowed. Allowed types: {FileManager.ALLOWED_EXTENSIONS}')
        
        # Create upload folder if it doesn't exist
        os.makedirs(FileManager.UPLOAD_FOLDER, exist_ok=True)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(FileManager.UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        return file_path
    
    @staticmethod
    def delete_file(file_path):
        """Delete a file"""
        if os.path.exists(file_path):
            os.remove(file_path)
