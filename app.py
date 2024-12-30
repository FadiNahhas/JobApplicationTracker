"""
Job Application Tracker - Main Application Entry Point

This module serves as the main entry point for the Job Application Tracker application.
It handles database initialization, schema updates, and application startup.

Key Functions:
- ensure_database_exists(): Creates/verifies database and updates schema
- update_database_schema(): Handles database migrations and schema updates
- load_resource_path(): Resolves paths for resources in both dev and built versions

Dependencies:
- PyQt6: For the GUI framework
- sqlite3: For database operations
- os, sys: For file and system operations
"""

import sys
import shutil
import os
import sqlite3
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from windows.main_window import MainWindow
from helpers.style_helper import load_stylesheet

def ensure_database_exists():
    """
    Ensures the application database exists and is properly initialized.
    Creates a new database from template if none exists.
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join("Data", "job_tracker.db")
    template_path = os.path.join(base_path, "Data", "job_tracker_template.db")

    # Create the database if it doesn't exist
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        shutil.copy(template_path, db_path)
    
    # Check and update database schema
    update_database_schema(db_path)

def update_database_schema(db_path):
    """
    Updates the database schema to the latest version.
    Handles creation of new tables and columns for features like locations.
    
    Args:
        db_path (str): Path to the database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if locations table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='locations'
        """)
        
        if not cursor.fetchone():
            # Create locations table
            cursor.execute("""
                CREATE TABLE locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT UNIQUE NOT NULL,
                    latitude REAL,
                    longitude REAL
                )
            """)
            
            # Add location_id column to applications table
            cursor.execute("""
                ALTER TABLE applications 
                ADD COLUMN location_id INTEGER 
                REFERENCES locations(id)
            """)
            
            print("Database schema updated with locations support")
        
        conn.commit()
    except Exception as e:
        print(f"Error updating database schema: {e}")
        conn.rollback()
    finally:
        conn.close()

# Call the function to ensure the database is present
ensure_database_exists()

def load_resource_path(relative_path):
    """
    Gets the absolute path to a resource, works for both development and PyInstaller builds.
    
    Args:
        relative_path (str): Relative path to the resource
        
    Returns:
        str: Absolute path to the resource
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extracts files to a temporary folder
        base_path = sys._MEIPASS
    else:
        # Use the current directory during development
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # Initialize Qt Application with OpenGL context sharing
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    # Set up application icon and styling
    icon_path = load_resource_path("assets/icon.ico")
    app.setWindowIcon(QIcon(icon_path))
    
    # Load and apply the application theme
    stylesheet = load_stylesheet("UI\ManjaroMix.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)
    
    # Launch the main window
    window = MainWindow()
    window.setWindowIcon(QIcon(icon_path))
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec())