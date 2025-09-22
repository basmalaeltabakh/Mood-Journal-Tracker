"""
Configuration and settings for the application
"""
class AppConfig:
    """Application configuration settings"""
    
    # Window settings
    WINDOW_TITLE = "Mood Journal Tracker"
    WINDOW_GEOMETRY = "800x600"
    BACKGROUND_COLOR = '#f0f0f0'
    
    # Data settings
    DATA_FILENAME = "journal.json"
    
    # Default moods
    DEFAULT_MOODS = [
        "Happy", "Sad", "Stressed", "Excited", "Calm", 
        "Anxious", "Tired", "Energetic", "Neutral"
    ]
    
    # UI settings
    DATE_FORMAT = "%Y-%m-%d"
    NOTES_PREVIEW_LENGTH = 50
    
    # Report settings
    CHART_FIGSIZE = (8, 4)
    TIMELINE_FIGSIZE = (10, 4)