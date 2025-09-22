"""
Validation utilities for the application
"""
from datetime import datetime
from Configuration.settings import AppConfig

class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_date(date_str):
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, AppConfig.DATE_FORMAT)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_mood(mood, allowed_moods):
        """Validate mood against allowed list"""
        return mood.strip() and mood.strip() in allowed_moods
    
    @staticmethod
    def validate_entry_data(entry_data, allowed_moods):
        """Validate complete entry data"""
        if not Validators.validate_date(entry_data.get('date', '')):
            return False, "Invalid date format"
        
        if not Validators.validate_mood(entry_data.get('mood', ''), allowed_moods):
            return False, "Invalid mood"
        
        return True, "Valid"