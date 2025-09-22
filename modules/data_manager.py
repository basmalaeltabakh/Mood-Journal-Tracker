"""
Data management module for handling journal entries
"""
import json
import os
from datetime import datetime
from tkinter import messagebox

class DataManager:
    """Handles all data operations for the mood journal"""
    
    def __init__(self, filename="journal.json"):
        self.filename = filename
        self.data = []
        self.initialize_data_file()
        self.load_data()
    
    def initialize_data_file(self):
        """Initialize the data file if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)
    
    def load_data(self):
        """Load journal data from file with error handling"""
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
                # Validate data structure
                for entry in self.data:
                    if 'date' not in entry or 'mood' not in entry:
                        raise ValueError("Invalid data structure in journal file")
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            messagebox.showwarning("Data Error", 
                                 f"Could not load journal data. Starting with empty journal.\nError: {str(e)}")
            self.data = []
            # Recreate the file with empty data
            with open(self.filename, 'w') as file:
                json.dump(self.data, file)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error loading data: {str(e)}")
            self.data = []
    
    def save_data(self):
        """Save journal data to file with error handling"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save data: {str(e)}")
            return False
    
    def add_entry(self, entry):
        """Add a new journal entry"""
        self.data.append(entry)
        return self.save_data()
    
    def delete_entry(self, index):
        """Delete an entry by index"""
        if 0 <= index < len(self.data):
            deleted_entry = self.data.pop(index)
            if self.save_data():
                return deleted_entry
            else:
                # Restore if save failed
                self.data.insert(index, deleted_entry)
        return None
    
    def get_entries(self, filters=None):
        """Get entries with optional filtering"""
        if not filters:
            return self.data.copy()
        
        filtered_data = self.data.copy()
        
        # Apply date range filter
        if filters.get('start_date'):
            filtered_data = [e for e in filtered_data if e['date'] >= filters['start_date']]
        if filters.get('end_date'):
            filtered_data = [e for e in filtered_data if e['date'] <= filters['end_date']]
        
        # Apply mood filter
        if filters.get('mood') and filters['mood'] != 'All':
            filtered_data = [e for e in filtered_data if e['mood'] == filters['mood']]
        
        return filtered_data
    
    def clear_all_data(self):
        """Clear all journal data"""
        self.data = []
        return self.save_data()
    
    def backup_data(self, backup_filename=None):
        """Create a backup of the data file"""
        if not backup_filename:
            backup_filename = f"journal_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(self.filename, 'r') as source, open(backup_filename, 'w') as target:
                target.write(source.read())
            return backup_filename
        except Exception as e:
            raise Exception(f"Failed to create backup: {str(e)}")
    
    def restore_data(self, backup_filename):
        """Restore data from a backup file"""
        try:
            with open(backup_filename, 'r') as file:
                backup_data = json.load(file)
            
            # Validate backup data structure
            for entry in backup_data:
                if 'date' not in entry or 'mood' not in entry:
                    raise ValueError("Invalid backup file structure")
            
            self.data = backup_data
            return self.save_data()
        except Exception as e:
            raise Exception(f"Failed to restore data: {str(e)}")