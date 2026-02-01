"""
Enhanced report generation utilities with modern styling
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Configuration.settings import AppConfig

class ReportGenerator:
    """Handles generation of various reports with enhanced visuals"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        # Set matplotlib style
        plt.style.use('seaborn-v0_8-pastel')
    
    def generate_summary_report(self, parent_frame):
        """Generate enhanced mood frequency bar chart"""
        mood_counts = {}
        for entry in self.data_manager.data:
            mood = entry["mood"]
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        fig, ax = plt.subplots(figsize=AppConfig.CHART_FIGSIZE, facecolor='white')
        moods = list(mood_counts.keys())
        counts = list(mood_counts.values())
        
        # Get colors for each mood
        colors = [AppConfig.MOOD_COLORS.get(mood, AppConfig.PRIMARY_COLOR) 
                 for mood in moods]
        
        bars = ax.bar(moods, counts, color=colors, edgecolor='white', linewidth=2)
        
        ax.set_xlabel("Mood", fontsize=12, fontweight='bold', 
                     color=AppConfig.TEXT_COLOR)
        ax.set_ylabel("Frequency", fontsize=12, fontweight='bold', 
                     color=AppConfig.TEXT_COLOR)
        ax.set_title("Mood Frequency Analysis", fontsize=14, fontweight='bold',
                    color=AppConfig.TEXT_COLOR, pad=20)
        
        # Add value labels on bars with better styling
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.3, 
                   str(count), ha='center', va='bottom',
                   fontweight='bold', fontsize=11,
                   color=AppConfig.TEXT_COLOR)
        
        # Style improvements
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(AppConfig.BORDER_COLOR)
        ax.spines['bottom'].set_color(AppConfig.BORDER_COLOR)
        ax.tick_params(colors=AppConfig.TEXT_COLOR)
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        return canvas
    
    def generate_timeline_report(self, parent_frame):
        """Generate enhanced mood timeline chart"""
        if not self.data_manager.data:
            return None
        
        # Sort data by date
        sorted_data = sorted(self.data_manager.data, key=lambda x: x['date'])
        
        dates = [entry['date'] for entry in sorted_data]
        moods = [entry['mood'] for entry in sorted_data]
        
        # Convert moods to numerical values for plotting
        unique_moods = sorted(set(moods))
        mood_map = {mood: i for i, mood in enumerate(unique_moods)}
        mood_values = [mood_map[mood] for mood in moods]
        
        fig, ax = plt.subplots(figsize=AppConfig.TIMELINE_FIGSIZE, facecolor='white')
        
        # Create line plot with markers
        ax.plot(range(len(dates)), mood_values, 
               marker='o', linestyle='-', linewidth=2.5,
               color=AppConfig.PRIMARY_COLOR, markersize=8,
               markerfacecolor=AppConfig.PRIMARY_COLOR_LIGHT,
               markeredgecolor=AppConfig.PRIMARY_COLOR,
               markeredgewidth=2)
        
        # Set y-axis
        ax.set_yticks(range(len(unique_moods)))
        ax.set_yticklabels([f"{AppConfig.MOOD_EMOJIS.get(m, '')} {m}" 
                           for m in unique_moods])
        
        # Set x-axis
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha='right')
        
        ax.set_xlabel("Date", fontsize=12, fontweight='bold',
                     color=AppConfig.TEXT_COLOR)
        ax.set_ylabel("Mood", fontsize=12, fontweight='bold',
                     color=AppConfig.TEXT_COLOR)
        ax.set_title("Mood Timeline", fontsize=14, fontweight='bold',
                    color=AppConfig.TEXT_COLOR, pad=20)
        
        # Style improvements
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(AppConfig.BORDER_COLOR)
        ax.spines['bottom'].set_color(AppConfig.BORDER_COLOR)
        ax.tick_params(colors=AppConfig.TEXT_COLOR)
        ax.grid(alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        return canvas
    def generate_weekly_report_text(self):
        """Generate weekly summary report text"""
        report_text = "📅 WEEKLY SUMMARY REPORT\n"
        report_text += "=" * 50 + "\n\n"
        
        if not self.data_manager.data:
            return report_text + "No data available.\n\nStart tracking your moods to see weekly patterns!"
        
        # Group by week and count moods
        weekly_data = {}
        for entry in self.data_manager.data:
            try:
                date = datetime.strptime(entry['date'], AppConfig.DATE_FORMAT)
                year, week, _ = date.isocalendar()
                week_key = f"{year}-W{week:02d}"
                
                if week_key not in weekly_data:
                    weekly_data[week_key] = {}
                
                mood = entry['mood']
                weekly_data[week_key][mood] = weekly_data[week_key].get(mood, 0) + 1
            except ValueError:
                continue
        
        for week, moods in sorted(weekly_data.items(), reverse=True):
            report_text += f"📌 Week {week}\n"
            report_text += "-" * 40 + "\n"
            
            total = sum(moods.values())
            for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
                emoji = AppConfig.MOOD_EMOJIS.get(mood, '')
                percentage = (count / total) * 100
                report_text += f"  {emoji} {mood}: {count} entries ({percentage:.1f}%)\n"
            
            report_text += f"  Total: {total} entries\n\n"
        
        return report_text
    
    def generate_monthly_report_text(self):
        """Generate monthly summary report text"""
        report_text = "🗓️ MONTHLY SUMMARY REPORT\n"
        report_text += "=" * 50 + "\n\n"
        
        if not self.data_manager.data:
            return report_text + "No data available.\n\nStart tracking your moods to see monthly patterns!"
        
        # Group by month and count moods
        monthly_data = {}
        for entry in self.data_manager.data:
            try:
                date = datetime.strptime(entry['date'], AppConfig.DATE_FORMAT)
                month_key = date.strftime("%Y-%m (%B)")
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = {}
                
                mood = entry['mood']
                monthly_data[month_key][mood] = monthly_data[month_key].get(mood, 0) + 1
            except ValueError:
                continue
        
        for month, moods in sorted(monthly_data.items(), reverse=True):
            report_text += f"📌 {month}\n"
            report_text += "-" * 40 + "\n"
            
            total = sum(moods.values())
            for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
                emoji = AppConfig.MOOD_EMOJIS.get(mood, '')
                percentage = (count / total) * 100
                report_text += f"  {emoji} {mood}: {count} entries ({percentage:.1f}%)\n"
            
            # Find dominant mood
            dominant_mood = max(moods.items(), key=lambda x: x[1])
            report_text += f"\n  🌟 Dominant mood: {AppConfig.MOOD_EMOJIS.get(dominant_mood[0], '')} {dominant_mood[0]}\n"
            report_text += f"  📊 Total: {total} entries\n\n"
        
        return report_text
    
    def generate_text_report(self, parent_frame, report_text):
        """Generate a text-based report in the given frame"""
        # Clear previous content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(parent_frame)
        text_frame.pack(fill='both', expand=True)
        
        text_widget = tk.Text(text_frame, 
                             wrap=tk.WORD, 
                             height=20,
                             font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL),
                             relief=tk.FLAT,
                             borderwidth=0,
                             padx=15,
                             pady=15,
                             bg='white',
                             fg=AppConfig.TEXT_COLOR)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, 
                                 command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, report_text)
        text_widget.config(state=tk.DISABLED)