"""
Main application window
"""
import tkinter as tk
from tkinter import ttk
from Configuration.settings import AppConfig
from modules.data_manager import DataManager
from utils.report_generator import ReportGenerator
from gui.tabs import AddEntryTab, ViewEntriesTab, ReportsTab, SettingsTab

class MoodJournalApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_style() # Call new style setup method
        
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
    
    def setup_style(self):
        """Setup the ttk styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam') # Choose a modern theme
        
        # General styles
        self.style.configure('.', font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL),
                             background=AppConfig.BACKGROUND_COLOR,
                             foreground=AppConfig.TEXT_COLOR)
        
        # Frame and LabelFrame styles
        self.style.configure('TFrame', background=AppConfig.BACKGROUND_COLOR)
        self.style.configure('TLabelframe', background=AppConfig.BACKGROUND_COLOR, bordercolor=AppConfig.BORDER_COLOR)
        self.style.configure('TLabelframe.Label', font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_HEADING, 'bold'),
                             background=AppConfig.BACKGROUND_COLOR, foreground=AppConfig.TEXT_COLOR)
        
        # Label styles
        self.style.configure('TLabel', background=AppConfig.BACKGROUND_COLOR, foreground=AppConfig.TEXT_COLOR)
        
        # Button styles
        self.style.configure('TButton', font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, 'bold'),
                             background=AppConfig.PRIMARY_COLOR, foreground='white',
                             padding=[10, 5]) # [left/right, top/bottom]
        self.style.map('TButton',
                       background=[('active', AppConfig.PRIMARY_COLOR_DARK), ('!disabled', AppConfig.PRIMARY_COLOR)],
                       foreground=[('active', 'white'), ('!disabled', 'white')])
        
        # Entry and Combobox styles
        self.style.configure('TEntry', fieldbackground='white', bordercolor=AppConfig.BORDER_COLOR)
        self.style.configure('TCombobox', fieldbackground='white', background='white', bordercolor=AppConfig.BORDER_COLOR)
        
        # Notebook (Tab) styles
        self.style.configure('TNotebook', background=AppConfig.BACKGROUND_COLOR, borderwidth=0)
        self.style.configure('TNotebook.Tab', font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, 'bold'),
                             background='#e0e0e0', foreground=AppConfig.TEXT_COLOR,
                             padding=[AppConfig.PADDING_X, AppConfig.INNER_PADDING])
        self.style.map('TNotebook.Tab',
                       background=[('selected', AppConfig.BACKGROUND_COLOR)],
                       foreground=[('selected', AppConfig.TEXT_COLOR)])
        
        # Treeview styles
        self.style.configure('Treeview.Heading', font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, 'bold'),
                             background='#e0e0e0', foreground=AppConfig.TEXT_COLOR)
        self.style.configure('Treeview', background='white', fieldbackground='white',
                             foreground=AppConfig.TEXT_COLOR, rowheight=25)
        self.style.map('Treeview',
                       background=[('selected', AppConfig.SECONDARY_COLOR)],
                       foreground=[('selected', 'white')])
        
        # Scrollbar styles
        self.style.configure('Vertical.TScrollbar', background=AppConfig.BORDER_COLOR, troughcolor=AppConfig.BACKGROUND_COLOR)
        self.style.map('Vertical.TScrollbar', background=[('active', AppConfig.PRIMARY_COLOR)])

    def create_gui(self):
        """Create the main GUI interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=AppConfig.PADDING_X, pady=AppConfig.PADDING_Y)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W,
                              bg=AppConfig.BACKGROUND_COLOR, fg=AppConfig.TEXT_COLOR,
                              font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_SMALL))
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
        
        # Reports Tab
        self.reports_tab = ReportsTab(
            self.notebook, self.data_manager, self.report_generator, self.status_var
        )
        self.notebook.add(self.reports_tab.get_tab(), text="Reports")
        
        # Settings Tab
        self.settings_tab = SettingsTab(
            self.notebook, self.data_manager, self.moods, self.status_var
        )
        self.notebook.add(self.settings_tab.get_tab(), text="Settings")
    
    def refresh_ui(self):
        """Refresh the UI with current data"""
        # Refresh entries list if the view entries tab exists
        if hasattr(self, 'view_entries_tab'):
            self.view_entries_tab.refresh_entries()
        
        self.status_var.set(f"Loaded {len(self.data_manager.data)} entries")
