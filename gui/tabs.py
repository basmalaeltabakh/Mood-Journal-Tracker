"""
Tab definitions for the main application
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
from Configuration.settings import AppConfig
from utils.validators import Validators
from gui.widgets import DateEntry, FilterFrame

class AddEntryTab:
    """Add Entry tab implementation"""
    
    def __init__(self, parent, data_manager, moods, status_var):
        self.parent = parent
        self.data_manager = data_manager
        self.moods = moods
        self.status_var = status_var
        self.create_tab()
    
    def create_tab(self):
        """Create the tab contents"""
        self.tab = ttk.Frame(self.parent)
        
        # Main frame
        main_frame = ttk.LabelFrame(self.tab, text="New Mood Entry", padding=15)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Date selection
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill='x', pady=5)
        
        self.date_entry = DateEntry(date_frame)
        self.date_entry.pack(side=tk.LEFT)
        
        # Mood selection
        mood_frame = ttk.Frame(main_frame)
        mood_frame.pack(fill='x', pady=5)
        
        ttk.Label(mood_frame, text="Mood:").pack(side=tk.LEFT)
        self.mood_var = tk.StringVar()
        self.mood_combo = ttk.Combobox(mood_frame, textvariable=self.mood_var, 
                                      values=self.moods, width=15)
        self.mood_combo.pack(side=tk.LEFT, padx=5)
        self.mood_combo.set("Happy")
        
        # Notes section
        notes_frame = ttk.LabelFrame(main_frame, text="Additional Notes (Optional)", padding=10)
        notes_frame.pack(fill='both', expand=True, pady=5)
        
        self.notes_text = tk.Text(notes_frame, height=8, width=50)
        self.notes_text.pack(fill='both', expand=True)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
    def add_entry(self):
        """Add a new journal entry"""
        try:
            date = self.date_entry.get_date()
            mood = self.mood_var.get().strip()
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            # Validate input
            if not Validators.validate_date(date):
                messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format")
                return
            
            if not mood or mood not in self.moods:
                messagebox.showerror("Invalid Mood", "Please select a valid mood")
                return
            
            # Create and save entry
            entry = {"date": date, "mood": mood, "notes": notes}
            
            if self.data_manager.add_entry(entry):
                messagebox.showinfo("Success", "Entry added successfully!")
                self.clear_form()
                self.status_var.set(f"Entry added for {entry['date']}")
            else:
                # Remove the entry if save failed
                if entry in self.data_manager.data:
                    self.data_manager.data.remove(entry)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {str(e)}")
    
    def clear_form(self):
        """Clear the form"""
        self.date_entry.set_today()
        self.mood_combo.set("Happy")
        self.notes_text.delete("1.0", tk.END)
    
    def get_tab(self):
        """Get the tab widget"""
        return self.tab

class ViewEntriesTab:
    """View Entries tab implementation"""
    
    def __init__(self, parent, data_manager, moods, status_var):
        self.parent = parent
        self.data_manager = data_manager
        self.moods = moods
        self.status_var = status_var
        self.create_tab()
    
    def create_tab(self):
        """Create the tab contents"""
        self.tab = ttk.Frame(self.parent)
        
        # Filter frame
        self.filter_frame = FilterFrame(self.tab, self.moods, padding=10)
        self.filter_frame.pack(fill='x', padx=10, pady=5)
        
        # Apply/Clear filter buttons
        filter_button_frame = ttk.Frame(self.tab)
        filter_button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(filter_button_frame, text="Apply Filters", 
                  command=self.apply_filters).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_button_frame, text="Clear Filters", 
                  command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        
        # Entries list
        list_frame = ttk.LabelFrame(self.tab, text="Journal Entries", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for entries
        columns = ("Date", "Mood", "Notes")
        self.entries_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.entries_tree.heading(col, text=col)
            self.entries_tree.column(col, width=100)
        
        self.entries_tree.column("Notes", width=300)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.entries_tree.yview)
        self.entries_tree.configure(yscrollcommand=scrollbar.set)
        self.entries_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_entries).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
    
    def refresh_entries(self, filters=None):
        """Refresh the entries list"""
        try:
            # Clear existing items
            for item in self.entries_tree.get_children():
                self.entries_tree.delete(item)
            
            # Get filtered data
            if filters is None:
                filters = self.filter_frame.get_filters()
            
            filtered_data = self.data_manager.get_entries(filters)
            
            # Add entries to treeview
            for entry in filtered_data:
                notes = entry.get('notes', '')
                if len(notes) > AppConfig.NOTES_PREVIEW_LENGTH:
                    notes = notes[:AppConfig.NOTES_PREVIEW_LENGTH] + "..."
                
                self.entries_tree.insert("", tk.END, values=(entry['date'], entry['mood'], notes))
            
            self.status_var.set(f"Displaying {len(filtered_data)} entries")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh entries: {str(e)}")
    
    def apply_filters(self):
        """Apply filters to the entries list"""
        filters = self.filter_frame.get_filters()
        self.refresh_entries(filters)
        self.status_var.set("Filters applied")
    
    def clear_filters(self):
        """Clear all filters"""
        self.filter_frame.clear_filters()
        self.refresh_entries()
        self.status_var.set("Filters cleared")
    
    def delete_entry(self):
        """Delete the selected entry"""
        try:
            selection = self.entries_tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an entry to delete")
                return
            
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?"):
                index = self.entries_tree.index(selection[0])
                deleted_entry = self.data_manager.delete_entry(index)
                
                if deleted_entry:
                    self.refresh_entries()
                    messagebox.showinfo("Success", "Entry deleted successfully")
                    self.status_var.set(f"Deleted entry from {deleted_entry['date']}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")
    
    def export_to_csv(self):
        """Export data to CSV file"""
        try:
            filename = simpledialog.askstring("Export CSV", "Enter filename (without extension):")
            if filename:
                if not filename.endswith('.csv'):
                    filename += '.csv'
                
                with open(filename, 'w') as file:
                    file.write("Date,Mood,Notes\n")
                    for entry in self.data_manager.data:
                        notes = entry.get('notes', '').replace('"', '""')
                        file.write(f'"{entry["date"]}","{entry["mood"]}","{notes}"\n')
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                self.status_var.set(f"Data exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
    
    def get_tab(self):
        """Get the tab widget"""
        return self.tab

# Additional tab classes (ReportsTab, SettingsTab) would follow similar patterns
# Due to length constraints, I've shown the pattern for the first two tabs