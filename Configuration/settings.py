"""
Configuration and settings for the application
"""
class AppConfig:
    """Application configuration settings"""
    
    # Window settings
    WINDOW_TITLE = "Mood Journal Tracker ✨"
    WINDOW_GEOMETRY = "1000x750"
    MIN_WIDTH = 900
    MIN_HEIGHT = 700
    
    # Modern Color Palette - Soft therapeutic theme with depth
    BACKGROUND_COLOR = '#f5f7fa'      # Soft off-white background
    CARD_BACKGROUND = '#ffffff'       # Pure white for cards
    PRIMARY_COLOR = '#6366f1'         # Modern indigo
    PRIMARY_COLOR_DARK = '#4f46e5'    # Darker indigo for hover
    PRIMARY_COLOR_LIGHT = '#818cf8'   # Light indigo for accents
    SECONDARY_COLOR = '#10b981'       # Emerald green for positive
    ACCENT_COLOR = '#f59e0b'          # Amber for highlights
    WARNING_COLOR = '#ef4444'         # Red for warnings
    TEXT_COLOR = '#1f2937'            # Dark gray for text
    TEXT_SECONDARY = '#6b7280'        # Medium gray for secondary text
    BORDER_COLOR = '#e5e7eb'          # Light gray for borders
    SHADOW_COLOR = 'rgba(0, 0, 0, 0.1)'
    
    # Mood-specific colors
    MOOD_COLORS = {
        "Happy": '#fbbf24',      # Yellow
        "Sad": '#60a5fa',        # Blue
        "Stressed": '#f87171',   # Red
        "Excited": '#fb923c',    # Orange
        "Calm": '#34d399',       # Green
        "Anxious": '#a78bfa',    # Purple
        "Tired": '#94a3b8',      # Slate
        "Energetic": '#f472b6',  # Pink
        "Neutral": '#9ca3af'     # Gray
    }
    
    # Font settings
    FONT_FAMILY = "Segoe UI"
    FONT_FAMILY_HEADING = "Segoe UI Semibold"
    FONT_SIZE_NORMAL = 11
    FONT_SIZE_LARGE = 16
    FONT_SIZE_SMALL = 9
    FONT_SIZE_HEADING = 14
    FONT_SIZE_TITLE = 20
    
    # Data settings
    DATA_FILENAME = "journal.json"
    
    # Default moods with emojis
    DEFAULT_MOODS = [
        "Happy", "Sad", "Stressed", "Excited", "Calm", 
        "Anxious", "Tired", "Energetic", "Neutral"
    ]
    
    MOOD_EMOJIS = {
        "Happy": "😊",
        "Sad": "😢",
        "Stressed": "😰",
        "Excited": "🤩",
        "Calm": "😌",
        "Anxious": "😟",
        "Tired": "😴",
        "Energetic": "⚡",
        "Neutral": "😐"
    }
    
    # UI settings
    DATE_FORMAT = "%Y-%m-%d"
    NOTES_PREVIEW_LENGTH = 50
    
    # Layout settings
    PADDING_X = 20
    PADDING_Y = 20
    INNER_PADDING = 15
    CARD_PADDING = 20
    BORDER_RADIUS = 12
    
    # Report settings
    CHART_FIGSIZE = (10, 5.5)
    TIMELINE_FIGSIZE = (12, 5.5)

    # ML Settings
    NEUTRAL_SENTIMENT = 0.0
    
    # Animation settings
    HOVER_RELIEF = 'raised'
    BUTTON_PADDING = (12, 8)