"""
Main application window with enhanced UI
"""
import tkinter as tk
from tkinter import ttk
from Configuration.settings import AppConfig
from modules.data_manager import DataManager
from utils.report_generator import ReportGenerator
from gui.tabs import AddEntryTab, ViewEntriesTab, ReportsTab, SettingsTab

class MoodJournalApp:
    """Main application class with modern UI"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_style()
        
        # Initialize components
        self.data_manager = DataManager(AppConfig.DATA_FILENAME)
        self.report_generator = ReportGenerator(self.data_manager)
        self.moods = AppConfig.DEFAULT_MOODS.copy()
        
        # Create GUI
        self.create_gui()
        
        # Load initial data
        self.refresh_ui()
    
    def setup_window(self):
        """Setup the main window with modern appearance"""
        self.root.title(AppConfig.WINDOW_TITLE)
        self.root.geometry(AppConfig.WINDOW_GEOMETRY)
        self.root.minsize(AppConfig.MIN_WIDTH, AppConfig.MIN_HEIGHT)
        self.root.configure(bg=AppConfig.BACKGROUND_COLOR)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_style(self):
        """Setup enhanced ttk styles for modern UI"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # General styles with modern look
        self.style.configure('.', 
                           font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL),
                           background=AppConfig.BACKGROUND_COLOR,
                           foreground=AppConfig.TEXT_COLOR)
        
        # Frame styles
        self.style.configure('TFrame', background=AppConfig.BACKGROUND_COLOR)
        
        self.style.configure('Card.TFrame', 
                           background=AppConfig.CARD_BACKGROUND,
                           relief='flat')
        
        # LabelFrame styles with card appearance
        self.style.configure('TLabelframe', 
                           background=AppConfig.CARD_BACKGROUND,
                           bordercolor=AppConfig.BORDER_COLOR,
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('TLabelframe.Label', 
                           font=(AppConfig.FONT_FAMILY_HEADING, AppConfig.FONT_SIZE_HEADING, 'bold'),
                           background=AppConfig.CARD_BACKGROUND, 
                           foreground=AppConfig.TEXT_COLOR,
                           padding=(0, 5))
        
        # Label styles
        self.style.configure('TLabel', 
                           background=AppConfig.CARD_BACKGROUND, 
                           foreground=AppConfig.TEXT_COLOR)
        
        self.style.configure('Title.TLabel',
                           font=(AppConfig.FONT_FAMILY_HEADING, AppConfig.FONT_SIZE_TITLE, 'bold'),
                           foreground=AppConfig.PRIMARY_COLOR)
        
        self.style.configure('Secondary.TLabel',
                           foreground=AppConfig.TEXT_SECONDARY,
                           font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_SMALL))
        
        # Modern button styles
        self.style.configure('TButton', 
                           font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, 'bold'),
                           background=AppConfig.PRIMARY_COLOR, 
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=AppConfig.BUTTON_PADDING,
                           relief='flat')
        
        self.style.map('TButton',
                      background=[('active', AppConfig.PRIMARY_COLOR_DARK), 
                                ('!disabled', AppConfig.PRIMARY_COLOR),
                                ('disabled', AppConfig.BORDER_COLOR)],
                      foreground=[('active', 'white'), 
                                ('!disabled', 'white'),
                                ('disabled', AppConfig.TEXT_SECONDARY)])
        
        # Secondary button style
        self.style.configure('Secondary.TButton',
                           background=AppConfig.BACKGROUND_COLOR,
                           foreground=AppConfig.TEXT_COLOR,
                           borderwidth=1)
        
        self.style.map('Secondary.TButton',
                      background=[('active', AppConfig.BORDER_COLOR),
                                ('!disabled', AppConfig.BACKGROUND_COLOR)])
        
        # Success button style
        self.style.configure('Success.TButton',
                           background=AppConfig.SECONDARY_COLOR)
        
        self.style.map('Success.TButton',
                      background=[('active', '#059669'),
                                ('!disabled', AppConfig.SECONDARY_COLOR)])
        
        # Warning button style
        self.style.configure('Warning.TButton',
                           background=AppConfig.WARNING_COLOR)
        
        self.style.map('Warning.TButton',
                      background=[('active', '#dc2626'),
                                ('!disabled', AppConfig.WARNING_COLOR)])
        
        # Entry and Combobox styles
        self.style.configure('TEntry', 
                           fieldbackground='white',
                           bordercolor=AppConfig.BORDER_COLOR,
                           lightcolor=AppConfig.BORDER_COLOR,
                           darkcolor=AppConfig.BORDER_COLOR,
                           borderwidth=1,
                           relief='flat')
        
        self.style.map('TEntry',
                      bordercolor=[('focus', AppConfig.PRIMARY_COLOR)])
        
        self.style.configure('TCombobox', 
                           fieldbackground='white',
                           background='white',
                           bordercolor=AppConfig.BORDER_COLOR,
                           arrowcolor=AppConfig.TEXT_COLOR,
                           borderwidth=1,
                           relief='flat')
        
        self.style.map('TCombobox',
                      bordercolor=[('focus', AppConfig.PRIMARY_COLOR)],
                      fieldbackground=[('readonly', 'white')],
                      selectbackground=[('readonly', 'white')],
                      selectforeground=[('readonly', AppConfig.TEXT_COLOR)])
        
        # Notebook (Tab) styles with modern look
        self.style.configure('TNotebook', 
                           background=AppConfig.BACKGROUND_COLOR,
                           borderwidth=0,
                           tabmargins=[5, 5, 5, 0])
        
        self.style.configure('TNotebook.Tab', 
                           font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, 'bold'),
                           background=AppConfig.BACKGROUND_COLOR,
                           foreground=AppConfig.TEXT_SECONDARY,
                           padding=[20, 10],
                           borderwidth=0)
        
        self.style.map('TNotebook.Tab',
                      background=[('selected', AppConfig.CARD_BACKGROUND)],
                      foreground=[('selected', AppConfig.PRIMARY_COLOR)],
                      expand=[('selected', [1, 1, 1, 0])])
        
        # Treeview styles
        self.style.configure('Treeview', 
                           background='white',
                           fieldbackground='white',
                           foreground=AppConfig.TEXT_COLOR,
                           borderwidth=0,
                           rowheight=32,
                           relief='flat')
        
        self.style.configure('Treeview.Heading', 
                           font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, 'bold'),
                           background=AppConfig.BACKGROUND_COLOR,
                           foreground=AppConfig.TEXT_COLOR,
                           borderwidth=0,
                           relief='flat')
        
        self.style.map('Treeview',
                      background=[('selected', AppConfig.PRIMARY_COLOR_LIGHT)],
                      foreground=[('selected', 'white')])
        
        self.style.map('Treeview.Heading',
                      background=[('active', AppConfig.BORDER_COLOR)])
        
        # Scrollbar styles
        self.style.configure('Vertical.TScrollbar', 
                           background=AppConfig.BORDER_COLOR,
                           troughcolor=AppConfig.BACKGROUND_COLOR,
                           borderwidth=0,
                           arrowcolor=AppConfig.TEXT_COLOR)
        
        self.style.map('Vertical.TScrollbar',
                      background=[('active', AppConfig.PRIMARY_COLOR)])

    def create_gui(self):
        """Create the main GUI interface with modern layout"""
        # Header section
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=AppConfig.PADDING_X, pady=(AppConfig.PADDING_Y, 10))
    
        title_label = ttk.Label(header_frame, 
                           text="✨ Mood Journal Tracker",
                           style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
    
        subtitle_label = ttk.Label(header_frame,
                              text="Track your emotions, understand your patterns",
                              style='Secondary.TLabel')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
    
        # ⚠️ مهم: اعملي status_var هنا الأول قبل الـ notebook!
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
    
    # Main content with notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, 
                      padx=AppConfig.PADDING_X, 
                      pady=(0, AppConfig.PADDING_Y))
    
        # Create tabs 
        self.create_tabs()
    
        # Modern status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
        status_bar = tk.Label(status_frame, 
                        textvariable=self.status_var,
                        relief=tk.FLAT,
                        anchor=tk.W,
                        bg=AppConfig.CARD_BACKGROUND,
                        fg=AppConfig.TEXT_SECONDARY,
                        font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_SMALL),
                        padx=AppConfig.PADDING_X,
                        pady=8)
        status_bar.pack(fill=tk.X)
    
    def create_tabs(self):
        """Create all application tabs"""
        # Add Entry Tab
        self.add_entry_tab = AddEntryTab(
            self.notebook, self.data_manager, self.moods, self.status_var
        )
        self.notebook.add(self.add_entry_tab.get_tab(), text="📝 Add Entry")
        
        # View Entries Tab
        self.view_entries_tab = ViewEntriesTab(
            self.notebook, self.data_manager, self.moods, self.status_var
        )
        self.notebook.add(self.view_entries_tab.get_tab(), text="📚 View Entries")
        
        # Reports Tab
        self.reports_tab = ReportsTab(
            self.notebook, self.data_manager, self.report_generator, self.status_var
        )
        self.notebook.add(self.reports_tab.get_tab(), text="📊 Reports")
        
        # Settings Tab
        self.settings_tab = SettingsTab(
            self.notebook, self.data_manager, self.moods, self.status_var
        )
        self.notebook.add(self.settings_tab.get_tab(), text="⚙️ Settings")
    
    def refresh_ui(self):
        """Refresh the UI with current data"""
        if hasattr(self, 'view_entries_tab'):
            self.view_entries_tab.refresh_entries()
        
        entry_count = len(self.data_manager.data)
        self.status_var.set(f"📊 {entry_count} {'entry' if entry_count == 1 else 'entries'} loaded")