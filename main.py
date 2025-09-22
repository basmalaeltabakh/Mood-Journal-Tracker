#!/usr/bin/env python3
"""
Main entry point for the Mood Journal Application
"""
import tkinter as tk
from tkinter import messagebox
from gui.main_window import MoodJournalApp

def main():
    """Main function to start the application"""
    try:
        root = tk.Tk()
        app = MoodJournalApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")

if __name__ == "__main__":
    main()