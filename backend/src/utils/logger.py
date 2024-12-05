import logging
import os
from datetime import datetime

class CustomLogger:
    """
    Custom logging utility with configurable logging levels
    """
    @staticmethod
    def setup_logger(name='autograder', 
                     log_level=logging.INFO, 
                     log_dir='logs'):
        """
        Create and configure a logger
        
        :param name: Name of the logger
        :param log_level: Logging level
        :param log_dir: Directory to store log files
        :return: Configured logger
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Generate log filename with timestamp
        log_filename = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        # Configure logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        # File handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger