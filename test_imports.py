"""
Test script to check if all imports are working correctly
"""
import sys
import traceback

print("=" * 50)
print("Testing Mood Journal Tracker Imports")
print("=" * 50)

# Test 1: Check Python version
print(f"\n1. Python Version: {sys.version}")

# Test 2: Test tkinter
try:
    import tkinter as tk
    from tkinter import ttk
    print("✓ tkinter imported successfully")
except Exception as e:
    print(f"✗ tkinter import failed: {e}")

# Test 3: Test matplotlib
try:
    import matplotlib
    import matplotlib.pyplot as plt
    print("✓ matplotlib imported successfully")
except Exception as e:
    print(f"✗ matplotlib import failed: {e}")

# Test 4: Test Configuration
try:
    from Configuration.settings import AppConfig
    print("✓ Configuration.settings imported successfully")
    print(f"  - Window Title: {AppConfig.WINDOW_TITLE}")
except Exception as e:
    print(f"✗ Configuration.settings import failed:")
    traceback.print_exc()

# Test 5: Test modules
try:
    from modules.data_manager import DataManager
    print("✓ modules.data_manager imported successfully")
except Exception as e:
    print(f"✗ modules.data_manager import failed:")
    traceback.print_exc()

# Test 6: Test utils
try:
    from utils.report_generator import ReportGenerator
    print("✓ utils.report_generator imported successfully")
except Exception as e:
    print(f"✗ utils.report_generator import failed:")
    traceback.print_exc()

try:
    from utils.validators import Validators
    print("✓ utils.validators imported successfully")
except Exception as e:
    print(f"✗ utils.validators import failed:")
    traceback.print_exc()

# Test 7: Test gui modules
try:
    from gui.widgets import DateEntry, FilterFrame, MoodButton
    print("✓ gui.widgets imported successfully")
except Exception as e:
    print(f"✗ gui.widgets import failed:")
    traceback.print_exc()

try:
    from gui.tabs import AddEntryTab, ViewEntriesTab, ReportsTab, SettingsTab
    print("✓ gui.tabs imported successfully")
except Exception as e:
    print(f"✗ gui.tabs import failed:")
    traceback.print_exc()

try:
    from gui.main_window import MoodJournalApp
    print("✓ gui.main_window imported successfully")
except Exception as e:
    print(f"✗ gui.main_window import failed:")
    traceback.print_exc()

print("\n" + "=" * 50)
print("Import test completed!")
print("=" * 50)