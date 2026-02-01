"""
ML Analyzer for sentiment analysis and insights
"""
from Configuration.settings import AppConfig

class MLAnalyzer:
    """Handles ML-based analysis for mood entries"""
    
    def __init__(self):
        pass
    
    def analyze_sentiment(self, notes):
        """Analyze sentiment of notes text"""
        try:
            if not notes.strip():
                return AppConfig.NEUTRAL_SENTIMENT, 0.0  # Neutral if no notes
            
            # Optional: Use TextBlob if available
            try:
                from textblob import TextBlob
                blob = TextBlob(notes)
                polarity = blob.sentiment.polarity  # -1.0 to +1.0
                subjectivity = blob.sentiment.subjectivity  # 0.0 to 1.0
                return polarity, subjectivity
            except ImportError:
                # If TextBlob not installed, return neutral
                return AppConfig.NEUTRAL_SENTIMENT, 0.0
                
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return AppConfig.NEUTRAL_SENTIMENT, 0.0
    
    def get_overall_sentiment_trend(self, entries):
        """Get average sentiment from recent entries (last 7)"""
        if not entries:
            return AppConfig.NEUTRAL_SENTIMENT
        
        recent = entries[-7:]  # Last 7 entries
        scores = [entry.get('sentiment_score', AppConfig.NEUTRAL_SENTIMENT) for entry in recent]
        return sum(scores) / len(scores) if scores else AppConfig.NEUTRAL_SENTIMENT
    
    def suggest_mood_prediction(self, avg_sentiment):
        """Simple rule-based prediction based on sentiment"""
        if avg_sentiment > 0.3:
            return "Positive trend - Keep up the good vibes! Suggested mood: Happy/Energetic"
        elif avg_sentiment < -0.3:
            return "Negative trend - Consider self-care. Suggested mood: Sad/Anxious"
        else:
            return "Neutral trend - Balanced day ahead. Suggested mood: Calm/Neutral"