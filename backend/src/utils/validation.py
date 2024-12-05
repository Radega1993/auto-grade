import json
from typing import Dict, Any

class Validator:
    """
    Utility class for input validation
    """
    @staticmethod
    def validate_criteria_file(file_path: str) -> Dict[str, Any]:
        """
        Validate the structure of the criteria JSON file
        
        :param file_path: Path to the JSON file with evaluation criteria
        :return: Validated criteria dictionary
        :raises ValueError: If file is invalid
        """
        try:
            with open(file_path, 'r') as f:
                criteria = json.load(f)
            
            # Basic validation
            if not isinstance(criteria, dict):
                raise ValueError("Criteria must be a JSON object")
            
            # Check for minimum required keys
            required_keys = ['coherencia', 'contenido', 'profundidad']
            for key in required_keys:
                if key not in criteria:
                    raise ValueError(f"Missing required key: {key}")
            
            return criteria
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        except IOError:
            raise ValueError("Cannot read criteria file")
