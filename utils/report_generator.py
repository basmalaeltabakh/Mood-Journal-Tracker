"""
Report generation utilities
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from Configuration.settings import AppConfig

class ReportGenerator:
    """Handles generation of various reports"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def generate_summary_report(self, parent_frame):
        """Generate mood frequency bar chart"""
        mood_counts = {}
        for entry in self.data_manager.data:
            mood = entry["mood"]
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        fig, ax = plt.subplots(figsize=AppConfig.CHART_FIGSIZE)
        moods = list(mood_counts.keys())
        counts = list(mood_counts.values())
        
        bars = ax.bar(moods, counts, color='skyblue')
        ax.set_xlabel("Mood")
        ax.set_ylabel("Frequency")
        ax.set_title("Mood Frequency Report")
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   str(count), ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        return canvas
    
    def generate_timeline_report(self, parent_frame):
        """Generate mood timeline chart"""
        # Sort data by date
        sorted_data = sorted(self.data_manager.data, key=lambda x: x['date'])
        
        dates = [entry['date'] for entry in sorted_data]
        moods = [entry['mood'] for entry in sorted_data]
        
        # Convert moods to numerical values for plotting
        unique_moods = list(set(moods))
        mood_map = {mood: i for i, mood in enumerate(unique_moods)}
        mood_values = [mood_map[mood] for mood in moods]
        
        fig, ax = plt.subplots(figsize=AppConfig.TIMELINE_FIGSIZE)
        ax.plot(dates, mood_values, marker='o', linestyle='-', color='purple')
        ax.set_yticks(range(len(unique_moods)))
        ax.set_yticklabels(unique_moods)
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood")
        ax.set_title("Mood Timeline Report")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        return canvas
    
    def generate_weekly_report_text(self):
        """Generate weekly summary report text"""
        report_text = "Weekly Summary Report\n\n"
        
        # Group by week and count moods
        weekly_data = {}
        for entry in self.data_manager.data:
            date = datetime.strptime(entry['date'], AppConfig.DATE_FORMAT)
            year, week, _ = date.isocalendar()
            week_key = f"{year}-W{week:02d}"
            
            if week_key not in weekly_data:
                weekly_data[week_key] = {}
            
            mood = entry['mood']
            weekly_data[week_key][mood] = weekly_data[week_key].get(mood, 0) + 1
        
        for week, moods in sorted(weekly_data.items()):
            report_text += f"Week {week}:\n"
            for mood, count in moods.items():
                report_text += f"  {mood}: {count} entries\n"
            report_text += "\n"
        
        return report_text
    
    def generate_monthly_report_text(self):
        """Generate monthly summary report text"""
        report_text = "Monthly Summary Report\n\n"
        
        # Group by month and count moods
        monthly_data = {}
        for entry in self.data_manager.data:
            date = datetime.strptime(entry['date'], AppConfig.DATE_FORMAT)
            month_key = date.strftime("%Y-%m")
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {}
            
            mood = entry['mood']
            monthly_data[month_key][mood] = monthly_data[month_key].get(mood, 0) + 1
        
        for month, moods in sorted(monthly_data.items()):
            report_text += f"Month {month}:\n"
            for mood, count in moods.items():
                report_text += f"  {mood}: {count} entries\n"
            report_text += "\n"
        
        return report_text