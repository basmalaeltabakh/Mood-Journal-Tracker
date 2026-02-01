"""
Enhanced tab definitions for the main application
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
from Configuration.settings import AppConfig
from utils.validators import Validators
from gui.widgets import DateEntry, FilterFrame, MoodButton

class AddEntryTab:
    """Enhanced Add Entry tab with modern UI"""
    
    def __init__(self, parent, data_manager, moods, status_var):
        self.parent = parent
        self.data_manager = data_manager
        self.moods = moods
        self.status_var = status_var
        self.selected_mood = None
        self.mood_buttons = {}
        self.create_tab()
    
    def create_tab(self):
        """Create the tab contents with card-based layout"""
        self.tab = ttk.Frame(self.parent, style='TFrame')
        
        # Scrollable container for content
        canvas = tk.Canvas(self.tab, bg=AppConfig.BACKGROUND_COLOR, 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main content card
        main_card = ttk.LabelFrame(scrollable_frame, text="Create New Entry", 
                                  padding=AppConfig.CARD_PADDING)
        main_card.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Date selection section
        date_section = ttk.Frame(main_card)
        date_section.pack(fill='x', pady=(0, 20))
        
        self.date_entry = DateEntry(date_section)
        self.date_entry.pack(side=tk.LEFT)
        
        # Mood selection section with grid of buttons
        mood_section = ttk.LabelFrame(main_card, text="How are you feeling?", 
                                     padding=15)
        mood_section.pack(fill='x', pady=(0, 20))
        
        # Create mood button grid
        mood_grid = ttk.Frame(mood_section)
        mood_grid.pack()
        
        cols = 3
        for idx, mood in enumerate(self.moods):
            row = idx // cols
            col = idx % cols
            
            mood_btn = MoodButton(mood_grid, mood, self.select_mood)
            mood_btn.grid(row=row, column=col, padx=5, pady=5)
            self.mood_buttons[mood] = mood_btn
        
        # Set default mood
        self.select_mood("Happy")
        
        # Notes section with better styling
        notes_section = ttk.LabelFrame(main_card, 
                                      text="What's on your mind? (Optional)",
                                      padding=15)
        notes_section.pack(fill='both', expand=True, pady=(0, 20))
        
        # Text widget with custom styling
        text_frame = ttk.Frame(notes_section)
        text_frame.pack(fill='both', expand=True)
        
        self.notes_text = tk.Text(text_frame, 
                                 height=8, 
                                 width=50,
                                 font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL),
                                 wrap=tk.WORD,
                                 relief=tk.FLAT,
                                 borderwidth=1,
                                 highlightthickness=1,
                                 highlightcolor=AppConfig.PRIMARY_COLOR,
                                 highlightbackground=AppConfig.BORDER_COLOR,
                                 padx=10,
                                 pady=10)
        self.notes_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        notes_scrollbar = ttk.Scrollbar(text_frame, command=self.notes_text.yview)
        self.notes_text.config(yscrollcommand=notes_scrollbar.set)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Character counter
        self.char_count_var = tk.StringVar(value="0 characters")
        char_label = ttk.Label(notes_section, 
                              textvariable=self.char_count_var,
                              style='Secondary.TLabel')
        char_label.pack(anchor=tk.E, pady=(5, 0))
        
        self.notes_text.bind('<KeyRelease>', self.update_char_count)
        
        # Action buttons
        button_frame = ttk.Frame(main_card)
        button_frame.pack(fill='x', pady=(0, 0))
        
        ttk.Button(button_frame, 
                  text="💾 Save Entry", 
                  command=self.add_entry,
                  style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, 
                  text="🗑️ Clear", 
                  command=self.clear_form,
                  style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def select_mood(self, mood):
        """Handle mood selection"""
        # Deselect all buttons
        for btn in self.mood_buttons.values():
            btn.deselect()
        
        # Select clicked button
        if mood in self.mood_buttons:
            self.mood_buttons[mood].select()
            self.selected_mood = mood
    
    def update_char_count(self, event=None):
        """Update character count label"""
        content = self.notes_text.get("1.0", tk.END).strip()
        char_count = len(content)
        self.char_count_var.set(f"{char_count} characters")
    
    def add_entry(self):
        """Add a new journal entry with validation"""
        try:
            date = self.date_entry.get_date()
            mood = self.selected_mood
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            # Validate input
            if not Validators.validate_date(date):
                messagebox.showerror("Invalid Date", 
                                   "Please enter a valid date in YYYY-MM-DD format")
                return
            
            if not mood or mood not in self.moods:
                messagebox.showerror("Invalid Mood", 
                                   "Please select a mood")
                return
            
            # Create and save entry
            entry = {"date": date, "mood": mood, "notes": notes}
            
            if self.data_manager.add_entry(entry):
                messagebox.showinfo("Success! 🎉", 
                                  "Your entry has been saved successfully!")
                self.clear_form()
                self.status_var.set(f"✅ Entry added for {entry['date']}")
            else:
                if entry in self.data_manager.data:
                    self.data_manager.data.remove(entry)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {str(e)}")
    
    def clear_form(self):
        """Clear the form to default values"""
        self.date_entry.set_today()
        self.select_mood("Happy")
        self.notes_text.delete("1.0", tk.END)
        self.update_char_count()
    
    def get_tab(self):
        """Get the tab widget"""
        return self.tab
class ViewEntriesTab:
    """Enhanced View Entries tab with modern table design"""
    
    def __init__(self, parent, data_manager, moods, status_var):
        self.parent = parent
        self.data_manager = data_manager
        self.moods = moods
        self.status_var = status_var
        self.create_tab()
    
    def create_tab(self):
        """Create the tab contents with improved layout"""
        self.tab = ttk.Frame(self.parent, style='TFrame')
        
        # Top section with filters
        top_frame = ttk.Frame(self.tab)
        top_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        # Filter card
        self.filter_frame = FilterFrame(top_frame, self.moods, padding=15)
        self.filter_frame.pack(fill='x', side=tk.LEFT, expand=True)
        
        # Filter buttons
        filter_button_frame = ttk.Frame(top_frame)
        filter_button_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(filter_button_frame, 
                  text="🔍 Apply", 
                  command=self.apply_filters,
                  style='TButton').pack(pady=(0, 5))
        
        ttk.Button(filter_button_frame, 
                  text="✖️ Clear", 
                  command=self.clear_filters,
                  style='Secondary.TButton').pack()
        
        # Entries list card
        list_card = ttk.LabelFrame(self.tab, text="Your Journal Entries", 
                                  padding=15)
        list_card.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Treeview with enhanced styling
        tree_frame = ttk.Frame(list_card)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ("Date", "Mood", "Notes")
        self.entries_tree = ttk.Treeview(tree_frame, 
                                        columns=columns, 
                                        show="headings", 
                                        selectmode='browse')
        
        # Configure columns
        self.entries_tree.heading("Date", text="📅 Date")
        self.entries_tree.heading("Mood", text="😊 Mood")
        self.entries_tree.heading("Notes", text="📝 Notes")
        
        self.entries_tree.column("Date", width=120, anchor=tk.W)
        self.entries_tree.column("Mood", width=120, anchor=tk.W)
        self.entries_tree.column("Notes", width=400, anchor=tk.W)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, 
                                 command=self.entries_tree.yview)
        self.entries_tree.configure(yscrollcommand=scrollbar.set)
        
        self.entries_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add alternating row colors
        self.entries_tree.tag_configure('oddrow', background='white')
        self.entries_tree.tag_configure('evenrow', background=AppConfig.BACKGROUND_COLOR)
        
        # Action buttons
        button_frame = ttk.Frame(list_card)
        button_frame.pack(fill='x', pady=(15, 0))
        
        ttk.Button(button_frame, 
                  text="🔄 Refresh", 
                  command=self.refresh_entries,
                  style='TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, 
                  text="🗑️ Delete", 
                  command=self.delete_entry,
                  style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, 
                  text="📥 Export CSV", 
                  command=self.export_to_csv,
                  style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Entry count label
        self.count_var = tk.StringVar(value="0 entries")
        count_label = ttk.Label(button_frame, 
                               textvariable=self.count_var,
                               style='Secondary.TLabel')
        count_label.pack(side=tk.RIGHT)
        
        # Initial refresh
        self.refresh_entries()
    
    def refresh_entries(self, filters=None):
        """Refresh the entries list with alternating colors"""
        try:
            # Clear existing items
            for item in self.entries_tree.get_children():
                self.entries_tree.delete(item)
            
            # Get filters
            if filters is None:
                filters = self.filter_frame.get_filters()
            
            # Filter data
            filtered_data = []
            for entry in self.data_manager.data:
                include = True
                
                if filters['start_date'] and entry['date'] < filters['start_date']:
                    include = False
                if filters['end_date'] and entry['date'] > filters['end_date']:
                    include = False
                if filters['mood'] != 'All' and entry['mood'] != filters['mood']:
                    include = False
                
                if include:
                    filtered_data.append(entry)
            
            # Sort by date (newest first)
            filtered_data.sort(key=lambda x: x['date'], reverse=True)
            
            # Add entries with alternating colors
            for idx, entry in enumerate(filtered_data):
                notes = entry.get('notes', '')
                if len(notes) > AppConfig.NOTES_PREVIEW_LENGTH:
                    notes = notes[:AppConfig.NOTES_PREVIEW_LENGTH] + "..."
                
                # Get mood emoji
                mood_display = f"{AppConfig.MOOD_EMOJIS.get(entry['mood'], '')} {entry['mood']}"
                
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.entries_tree.insert("", tk.END, 
                                        values=(entry['date'], mood_display, notes),
                                        tags=(tag,))
            
            # Update count
            self.count_var.set(f"{len(filtered_data)} {'entry' if len(filtered_data) == 1 else 'entries'}")
            self.status_var.set(f"📊 Displaying {len(filtered_data)} entries")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh entries: {str(e)}")
    
    def apply_filters(self):
        """Apply filters to the entries list"""
        filters = self.filter_frame.get_filters()
        self.refresh_entries(filters)
        self.status_var.set("🔍 Filters applied")
    
    def clear_filters(self):
        """Clear all filters"""
        self.filter_frame.clear_filters()
        self.refresh_entries()
        self.status_var.set("✖️ Filters cleared")
    
    def delete_entry(self):
        """Delete the selected entry"""
        try:
            selection = self.entries_tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", 
                                     "Please select an entry to delete")
                return
            
            if messagebox.askyesno("Confirm Delete", 
                                  "Are you sure you want to delete this entry?"):
                selected_item = selection[0]
                item_values = self.entries_tree.item(selected_item, 'values')
                date = item_values[0]
                mood_display = item_values[1]
                
                # Extract mood name (remove emoji)
                mood = mood_display.split(' ', 1)[1] if ' ' in mood_display else mood_display
                
                # Find and delete the entry
                for i, entry in enumerate(self.data_manager.data):
                    if entry['date'] == date and entry['mood'] == mood:
                        deleted_entry = self.data_manager.delete_entry(i)
                        if deleted_entry:
                            self.refresh_entries()
                            messagebox.showinfo("Success", "Entry deleted successfully!")
                            self.status_var.set(f"🗑️ Deleted entry from {deleted_entry['date']}")
                        break
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")
    
    def export_to_csv(self):
        """Export data to CSV file"""
        try:
            filename = simpledialog.askstring("Export CSV", 
                                            "Enter filename (without extension):")
            if filename:
                if not filename.endswith('.csv'):
                    filename += '.csv'
                
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("Date,Mood,Notes\n")
                    for entry in self.data_manager.data:
                        notes = entry.get('notes', '').replace('"', '""')
                        file.write(f'"{entry["date"]}","{entry["mood"]}","{notes}"\n')
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                self.status_var.set(f"📥 Exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def get_tab(self):
        """Get the tab widget"""
        return self.tab    
class ReportsTab:
    """Enhanced Reports tab with modern visualization options"""
    
    def __init__(self, parent, data_manager, report_generator, status_var):
        self.parent = parent
        self.data_manager = data_manager
        self.report_generator = report_generator
        self.status_var = status_var
        self.create_tab()
    
    def create_tab(self):
        """Create the tab contents with modern layout"""
        self.tab = ttk.Frame(self.parent, style='TFrame')
        
        # Report options card
        options_card = ttk.LabelFrame(self.tab, 
                                     text="📊 Report Options", 
                                     padding=20)
        options_card.pack(fill='x', padx=15, pady=15)
        
        # Report type selection
        self.report_var = tk.StringVar(value="summary")
        
        # Create a grid of radio buttons
        radio_frame = ttk.Frame(options_card)
        radio_frame.pack(fill='x')
        
        reports = [
            ("summary", "📊 Mood Frequency", "See how often you feel each mood"),
            ("timeline", "📈 Mood Timeline", "Track your mood changes over time"),
            ("weekly", "📅 Weekly Summary", "Group entries by week"),
            ("monthly", "🗓️ Monthly Summary", "Group entries by month")
        ]
        
        for idx, (value, text, desc) in enumerate(reports):
            row = idx // 2
            col = idx % 2
            
            frame = ttk.Frame(radio_frame)
            frame.grid(row=row, column=col, sticky=tk.W, padx=10, pady=5)
            
            ttk.Radiobutton(frame, 
                          text=text,
                          variable=self.report_var, 
                          value=value).pack(anchor=tk.W)
            
            ttk.Label(frame, 
                     text=desc,
                     style='Secondary.TLabel').pack(anchor=tk.W, padx=(20, 0))
        
        # Generate button
        btn_frame = ttk.Frame(options_card)
        btn_frame.pack(fill='x', pady=(15, 0))
        
        ttk.Button(btn_frame, 
                  text="📊 Generate Report", 
                  command=self.generate_report,
                  style='Success.TButton').pack(side=tk.LEFT)
        
        ttk.Label(btn_frame,
                 text="Select a report type and click generate",
                 style='Secondary.TLabel').pack(side=tk.LEFT, padx=(15, 0))
        
        # Report display area
        display_card = ttk.LabelFrame(self.tab, 
                                     text="Report Visualization", 
                                     padding=15)
        display_card.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.report_frame = ttk.Frame(display_card)
        self.report_frame.pack(fill='both', expand=True)
        
        # Placeholder message
        placeholder = ttk.Label(self.report_frame,
                               text="📊\n\nSelect a report type and click 'Generate Report'\nto view your mood insights",
                               style='Secondary.TLabel',
                               font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_LARGE),
                               justify=tk.CENTER)
        placeholder.pack(expand=True)
    
    def generate_report(self):
        """Generate the selected report"""
        try:
            # Clear previous report
            for widget in self.report_frame.winfo_children():
                widget.destroy()
            
            if not self.data_manager.data:
                messagebox.showwarning("No Data", 
                                     "No journal entries available for reporting.\n\n" +
                                     "Add some entries first!")
                return
            
            report_type = self.report_var.get()
            
            if report_type == "summary":
                self.report_generator.generate_summary_report(self.report_frame)
            elif report_type == "timeline":
                self.report_generator.generate_timeline_report(self.report_frame)
            elif report_type == "weekly":
                report_text = self.report_generator.generate_weekly_report_text()
                self.report_generator.generate_text_report(self.report_frame, report_text)
            elif report_type == "monthly":
                report_text = self.report_generator.generate_monthly_report_text()
                self.report_generator.generate_text_report(self.report_frame, report_text)
            
            self.status_var.set(f"📊 Generated {report_type} report")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def get_tab(self):
        """Get the tab widget"""
        return self.tab
class SettingsTab:
    """Enhanced Settings tab with modern card layout"""
    
    def __init__(self, parent, data_manager, moods, status_var):
        self.parent = parent
        self.data_manager = data_manager
        self.moods = moods
        self.status_var = status_var
        self.create_tab()
    
    def create_tab(self):
        """Create the tab contents"""
        self.tab = ttk.Frame(self.parent, style='TFrame')
        
        # Scrollable container
        canvas = tk.Canvas(self.tab, bg=AppConfig.BACKGROUND_COLOR, 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Data management card
        data_card = ttk.LabelFrame(scrollable_frame, 
                                  text="💾 Data Management", 
                                  padding=20)
        data_card.pack(fill='x', padx=15, pady=(15, 10))
        
        ttk.Label(data_card,
                 text="Backup and manage your journal data",
                 style='Secondary.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        button_container = ttk.Frame(data_card)
        button_container.pack(fill='x')
        
        ttk.Button(button_container, 
                  text="💾 Backup Data", 
                  command=self.backup_data,
                  style='TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_container, 
                  text="📥 Restore Data", 
                  command=self.restore_data,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_container, 
                  text="🗑️ Clear All", 
                  command=self.clear_all_data,
                  style='Warning.TButton').pack(side=tk.LEFT)
        
        # Custom moods card
        moods_card = ttk.LabelFrame(scrollable_frame, 
                                   text="😊 Custom Moods", 
                                   padding=20)
        moods_card.pack(fill='x', padx=15, pady=(0, 10))
        
        ttk.Label(moods_card,
                 text="Add your own mood options",
                 style='Secondary.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        input_frame = ttk.Frame(moods_card)
        input_frame.pack(fill='x')
        
        ttk.Label(input_frame, text="New mood:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.custom_mood_var = tk.StringVar()
        mood_entry = ttk.Entry(input_frame, 
                              textvariable=self.custom_mood_var, 
                              width=20)
        mood_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(input_frame, 
                  text="➕ Add", 
                  command=self.add_custom_mood,
                  style='Success.TButton').pack(side=tk.LEFT)
        
        # Current moods display
        current_frame = ttk.Frame(moods_card)
        current_frame.pack(fill='x', pady=(15, 0))
        
        ttk.Label(current_frame, 
                 text="Current moods:",
                 style='Secondary.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        moods_text = tk.Text(current_frame, 
                            height=4, 
                            wrap=tk.WORD,
                            font=(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_SMALL),
                            relief=tk.FLAT,
                            bg=AppConfig.BACKGROUND_COLOR,
                            fg=AppConfig.TEXT_COLOR)
        moods_text.pack(fill='x')
        
        mood_list = ", ".join([f"{AppConfig.MOOD_EMOJIS.get(m, '')} {m}" 
                              for m in self.moods])
        moods_text.insert("1.0", mood_list)
        moods_text.config(state=tk.DISABLED)
        
        # About card
        about_card = ttk.LabelFrame(scrollable_frame, 
                                   text="ℹ️ About", 
                                   padding=20)
        about_card.pack(fill='x', padx=15, pady=(0, 15))
        
        about_text = """Mood Journal Tracker v2.0
        
Track your daily moods and generate insightful reports to understand your emotional patterns better.

✨ Features:
- Modern, intuitive interface
- Mood tracking with visual indicators
- Comprehensive reporting
- Data backup and export
- Customizable mood options

Made with ❤️ for your mental wellness"""
        
        ttk.Label(about_card, 
                 text=about_text,
                 justify=tk.LEFT,
                 style='Secondary.TLabel').pack(anchor=tk.W)
        
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def backup_data(self):
        """Create a backup of the data file"""
        try:
            backup_name = self.data_manager.backup_data()
            messagebox.showinfo("Backup Complete", 
                              f"✅ Backup created successfully!\n\n{backup_name}")
            self.status_var.set(f"💾 Backup created: {backup_name}")
        except Exception as e:
            messagebox.showerror("Backup Error", 
                               f"Failed to create backup:\n{str(e)}")
    
    def restore_data(self):
        """Restore data from a backup file"""
        try:
            filename = filedialog.askopenfilename(
                title="Select backup file", 
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                if self.data_manager.restore_data(filename):
                    messagebox.showinfo("Restore Complete", 
                                      "✅ Data restored successfully!")
                    self.status_var.set("📥 Data restored from backup")
                else:
                    messagebox.showerror("Restore Error", 
                                       "Failed to restore data")
                    
        except Exception as e:
            messagebox.showerror("Restore Error", 
                               f"Failed to restore data:\n{str(e)}")
    
    def clear_all_data(self):
        """Clear all journal data"""
        if messagebox.askyesno("Confirm Clear", 
                              "⚠️ Are you sure you want to delete ALL journal entries?\n\n" +
                              "This action cannot be undone!"):
            if self.data_manager.clear_all_data():
                messagebox.showinfo("Success", "All data cleared")
                self.status_var.set("🗑️ All data cleared")
            else:
                messagebox.showerror("Error", "Failed to clear data")
    
    def add_custom_mood(self):
        """Add a custom mood to the available moods list"""
        custom_mood = self.custom_mood_var.get().strip()
        
        if not custom_mood:
            messagebox.showwarning("Invalid", "Please enter a mood name")
            return
            
        if custom_mood in self.moods:
            messagebox.showwarning("Duplicate", 
                                 "This mood already exists")
            return
        
        self.moods.append(custom_mood)
        self.custom_mood_var.set("")
        messagebox.showinfo("Success", 
                          f"✅ Custom mood '{custom_mood}' added successfully!")
        self.status_var.set(f"➕ Added custom mood: {custom_mood}")
        
        # Refresh the mood display
        self.create_tab()
    
    def get_tab(self):
        """Get the tab widget"""
        return self.tab