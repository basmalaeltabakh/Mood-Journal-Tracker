"""
Configuration and settings for the application
"""
class AppConfig:
    """Application configuration settings"""
    
    # Window settings
    WINDOW_TITLE = "Mood Journal Tracker "
    WINDOW_GEOMETRY = "900x700"  # Slightly larger for new elements
    
    # Color Palette (Calming blue theme)
    BACKGROUND_COLOR = '#e8f4f8'  # Soft light blue for tranquility
    PRIMARY_COLOR = '#2196F3'     # Blue for main accents/buttons
    PRIMARY_COLOR_DARK = '#1976D2' # Darker blue for active states
    SECONDARY_COLOR = '#4CAF50'   # Green for positive elements (e.g., sentiment)
    TEXT_COLOR = '#2c3e50'        # Darker gray for better contrast on light bg
    ACCENT_COLOR = '#FF6B6B'      # Red/orange for warnings/negative sentiment
    BORDER_COLOR = '#b0bec5'      # Softer gray for borders
    
    # Font settings
    FONT_FAMILY = "Segoe UI"  # Or 'Arial', 'Helvetica'
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_LARGE = 14      # Larger for title
    FONT_SIZE_SMALL = 9
    FONT_SIZE_HEADING = 12
    
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
    
    # Layout settings
    PADDING_X = 15  # Increased for better breathing room
    PADDING_Y = 15
    INNER_PADDING = 8
    
    # Report settings
    CHART_FIGSIZE = (9, 5)   # Slightly larger
    TIMELINE_FIGSIZE = (12, 5)

    # ML Settings
    NEUTRAL_SENTIMENT = 0.0