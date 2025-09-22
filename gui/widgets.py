"""
Custom widgets for the application
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Configuration.settings import AppConfig

class DateEntry(ttk.Frame):
    """Custom date entry widget with today button"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()
    
    def create_widgets(self):
        """Create widget components"""
        ttk.Label(self, text="Date:").pack(side=tk.LEFT)
        
        self.date_var = tk.StringVar(value=datetime.today().strftime(AppConfig.DATE_FORMAT))
        self.entry = ttk.Entry(self, textvariable=self.date_var, width=15)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self, text="Today", command=self.set_today).pack(side=tk.LEFT, padx=5)
    
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
    """Filter frame for entry viewing"""
    
    def __init__(self, parent, moods, **kwargs):
        super().__init__(parent, text="Filters", **kwargs)
        self.moods = moods
        self.create_widgets()
    
    def create_widgets(self):
        """Create filter widgets"""
        # Date range
        ttk.Label(self, text="Date Range:").grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar(value=datetime.today().strftime(AppConfig.DATE_FORMAT))
        
        ttk.Entry(self, textvariable=self.start_date_var, width=12).grid(row=0, column=1, padx=5)
        ttk.Label(self, text="to").grid(row=0, column=2, padx=5)
        ttk.Entry(self, textvariable=self.end_date_var, width=12).grid(row=0, column=3, padx=5)
        
        # Mood filter
        ttk.Label(self, text="Mood:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.mood_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.mood_var, 
                    values=["All"] + self.moods, width=12).grid(row=0, column=5, padx=5)
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