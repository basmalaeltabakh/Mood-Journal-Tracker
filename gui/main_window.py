"""
Main application window
"""
import tkinter as tk
from tkinter import ttk
from Configuration.settings import AppConfig
from modules.data_manager import DataManager
from utils.report_generator import ReportGenerator
from gui.tabs import AddEntryTab, ViewEntriesTab

class MoodJournalApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Initialize components
        self.data_manager = DataManager(AppConfig.DATA_FILENAME)
        self.report_generator = ReportGenerator(self.data_manager)
        self.moods = AppConfig.DEFAULT_MOODS.copy()
        
        # Create GUI
        self.create_gui()
        
        # Load initial data
        self.refresh_ui()
    
    def setup_window(self):
        """Setup the main window"""
        self.root.title(AppConfig.WINDOW_TITLE)
        self.root.geometry(AppConfig.WINDOW_GEOMETRY)
        self.root.configure(bg=AppConfig.BACKGROUND_COLOR)
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create tabs
        self.create_tabs()
    
    def create_tabs(self):
        """Create all application tabs"""
        # Add Entry Tab
        self.add_entry_tab = AddEntryTab(
            self.notebook, self.data_manager, self.moods, self.status_var
        )
        self.notebook.add(self.add_entry_tab.get_tab(), text="Add Entry")
        
        # View Entries Tab
        self.view_entries_tab = ViewEntriesTab(
            self.notebook, self.data_manager, self.moods, self.status_var
        )
        self.notebook.add(self.view_entries_tab.get_tab(), text="View Entries")
        
        # Additional tabs would be added here following the same pattern
    
    def refresh_ui(self):
        """Refresh the UI with current data"""
        # Refresh entries list if the view entries tab is active
        if hasattr(self, 'view_entries_tab'):
            self.view_entries_tab.refresh_entries()
        
        self.status_var.set(f"Loaded {len(self.data_manager.data)} entries")