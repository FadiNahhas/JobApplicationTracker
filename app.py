import sys
import shutil
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from windows.main_window import MainWindow
from helpers.style_helper import load_stylesheet

def ensure_database_exists():
    # Determine the correct path for the template database
    if getattr(sys, 'frozen', False):  # Check if running as a bundled executable
        base_path = sys._MEIPASS  # Temp folder for PyInstaller bundled files
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join("Data", "job_tracker.db")
    template_path = os.path.join(base_path, "Data", "job_tracker_template.db")

    # Create the database if it doesn't exist
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure Data folder exists
        shutil.copy(template_path, db_path)

# Call the function to ensure the database is present
ensure_database_exists()

def load_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for both development and PyInstaller builds.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extracts files to a temporary folder
        base_path = sys._MEIPASS
    else:
        # Use the current directory during development
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application icon
    icon_path = load_resource_path("assets/icon.ico")
    app.setWindowIcon(QIcon(icon_path))

    # Load and apply the stylesheet
    stylesheet = load_stylesheet("UI\ManjaroMix.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)
    else:
        print("Failed to apply stylesheet.")

    # Initialize and display the main window
    window = MainWindow()
    window.setWindowIcon(QIcon(icon_path))
    window.show()

    sys.exit(app.exec())