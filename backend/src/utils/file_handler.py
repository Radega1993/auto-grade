import os
import uuid
from werkzeug.utils import secure_filename

class FileHandler:
    """
    Utility class for handling file operations
    """
    @staticmethod
    def generate_unique_filename(filename):
        """
        Generate a unique filename to prevent overwriting
        """
        unique_id = str(uuid.uuid4())
        return f"{unique_id}_{secure_filename(filename)}"

    @staticmethod
    def save_uploaded_file(file, upload_folder):
        """
        Save an uploaded file with a unique name
        
        :param file: File object from the request
        :param upload_folder: Directory to save the file
        :return: Path to the saved file
        """
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filename = FileHandler.generate_unique_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path

    @staticmethod
    def clean_temporary_files(file_paths, max_age_hours=24):
        """
        Remove temporary files older than specified hours
        
        :param file_paths: List of file paths to potentially delete
        :param max_age_hours: Maximum age of files before deletion
        """
        current_time = os.path.getctime()
        for file_path in file_paths:
            file_age = (current_time - os.path.getctime(file_path)) / 3600
            if file_age > max_age_hours:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
