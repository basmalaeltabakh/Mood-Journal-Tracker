"""
Custom widgets for the application with modern styling
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Configuration.settings import AppConfig

class DateEntry(ttk.Frame):
    """Enhanced date entry widget with calendar button"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()
    
    def create_widgets(self):
        """Create widget components with modern styling"""
        # Label with icon
        label = ttk.Label(self, text="📅 Date:", font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL))
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Date entry field
        self.date_var = tk.StringVar(value=datetime.today().strftime(AppConfig.DATE_FORMAT))
        self.entry = ttk.Entry(self, textvariable=self.date_var, width=12)
        self.entry.pack(side=tk.LEFT, padx=(0, 8))
        
        # Today button
        today_btn = ttk.Button(self, text="Today", command=self.set_today, style='Secondary.TButton')
        today_btn.pack(side=tk.LEFT)
    
    def set_today(self):
        """Set date to today"""
        self.date_var.set(datetime.today().strftime(AppConfig.DATE_FORMAT))
    
    def get_date(self):
        """Get current date value"""
        return self.date_var.get()
    
    def set_date(self, date_str):
        """Set date value"""
        self.date_var.set(date_str)


class FilterFrame(ttk.LabelFrame):
    """Enhanced filter frame for entry viewing"""
    
    def __init__(self, parent, moods, **kwargs):
        super().__init__(parent, text="🔍 Filters", **kwargs)
        self.moods = moods
        self.create_widgets()
    
    def create_widgets(self):
        """Create filter widgets with modern layout"""
        # Container for better spacing
        container = ttk.Frame(self)
        container.pack(fill='x', padx=10, pady=10)
        
        # Date range section
        date_frame = ttk.Frame(container)
        date_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(date_frame, text="Date Range:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.start_date_var = tk.StringVar()
        start_entry = ttk.Entry(date_frame, textvariable=self.start_date_var, width=12)
        start_entry.pack(side=tk.LEFT, padx=(0, 8))
        
        ttk.Label(date_frame, text="to", foreground=AppConfig.TEXT_SECONDARY).pack(side=tk.LEFT, padx=(0, 8))
        
        self.end_date_var = tk.StringVar(value=datetime.today().strftime(AppConfig.DATE_FORMAT))
        end_entry = ttk.Entry(date_frame, textvariable=self.end_date_var, width=12)
        end_entry.pack(side=tk.LEFT)
        
        # Mood filter section
        mood_frame = ttk.Frame(container)
        mood_frame.pack(fill='x')
        
        ttk.Label(mood_frame, text="Mood Filter:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.mood_var = tk.StringVar()
        mood_combo = ttk.Combobox(mood_frame, textvariable=self.mood_var, 
                                 values=["All"] + self.moods, width=15, state='readonly')
        mood_combo.pack(side=tk.LEFT)
        self.mood_var.set("All")
    
    def get_filters(self):
        """Get current filter values"""
        return {
            'start_date': self.start_date_var.get(),
            'end_date': self.end_date_var.get(),
            'mood': self.mood_var.get()
        }
    
    def clear_filters(self):
        """Clear all filters"""
        self.start_date_var.set("")
        self.end_date_var.set(datetime.today().strftime(AppConfig.DATE_FORMAT))
        self.mood_var.set("All")


class MoodButton(tk.Canvas):
    """Custom mood selection button with color and emoji"""
    
    def __init__(self, parent, mood, command, **kwargs):
        self.mood = mood
        self.command = command
        self.is_selected = False
        
        # Get mood color
        self.color = AppConfig.MOOD_COLORS.get(mood, AppConfig.TEXT_SECONDARY)
        self.emoji = AppConfig.MOOD_EMOJIS.get(mood, "")
        
        super().__init__(parent, width=100, height=80, 
                        highlightthickness=0, **kwargs)
        
        self.create_button()
        self.bind('<Button-1>', lambda e: self.on_click())
        self.bind('<Enter>', lambda e: self.on_hover())
        self.bind('<Leave>', lambda e: self.on_leave())
    
    def create_button(self):
        """Create the button visual elements"""
        # Background
        self.bg_rect = self.create_rectangle(2, 2, 98, 78,
                                            fill='white',
                                            outline=AppConfig.BORDER_COLOR,
                                            width=2)
        
        # Emoji
        self.create_text(50, 30, text=self.emoji, 
                        font=(AppConfig.FONT_FAMILY, 24))
        
        # Mood text
        self.create_text(50, 60, text=self.mood,
                        font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_SMALL),
                        fill=AppConfig.TEXT_COLOR)
    
    def on_click(self):
        """Handle click event"""
        self.command(self.mood)
    
    def on_hover(self):
        """Handle hover state"""
        if not self.is_selected:
            self.itemconfig(self.bg_rect, fill=AppConfig.BACKGROUND_COLOR)
    
    def on_leave(self):
        """Handle leave state"""
        if not self.is_selected:
            self.itemconfig(self.bg_rect, fill='white')
    
    def select(self):
        """Mark as selected"""
        self.is_selected = True
        self.itemconfig(self.bg_rect, fill=self.color, outline=self.color, width=3)
    
    def deselect(self):
        """Mark as deselected"""
        self.is_selected = False
        self.itemconfig(self.bg_rect, fill='white', 
                       outline=AppConfig.BORDER_COLOR, width=2)


class StatsCard(ttk.Frame):
    """Card widget for displaying statistics"""
    
    def __init__(self, parent, title, value, icon="📊", color=None, **kwargs):
        super().__init__(parent, style='Card.TFrame', **kwargs)
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color or AppConfig.PRIMARY_COLOR
        
        self.create_card()
    
    def create_card(self):
        """Create the card layout"""
        # Icon
        icon_label = ttk.Label(self, text=self.icon,
                              font=(AppConfig.FONT_FAMILY, 32))
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ttk.Label(self, text=str(self.value),
                               font=(AppConfig.FONT_FAMILY_HEADING, 24, 'bold'),
                               foreground=self.color)
        value_label.pack()
        
        # Title
        title_label = ttk.Label(self, text=self.title,
                               style='Secondary.TLabel')
        title_label.pack(pady=(5, 15))
    
    def update_value(self, new_value):
        """Update the displayed value"""
        self.value = new_value
        for widget in self.winfo_children():
            widget.destroy()
        self.create_card()