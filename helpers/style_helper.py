import os
import sys

def load_stylesheet(relative_path):
    """
    Load a stylesheet, resolving paths for both development and bundled builds.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extracts files to a temporary folder
        base_path = sys._MEIPASS
    else:
        # Use the current directory during development
        base_path = ""
    stylesheet_path = os.path.join(base_path, relative_path)

    # Debug: Verify the resolved path
    print(f"Loading stylesheet from: {stylesheet_path}")

    # Read and return the stylesheet content
    try:
        with open(stylesheet_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Stylesheet not found at: {stylesheet_path}")
        return ""