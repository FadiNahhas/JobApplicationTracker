# Job Application Tracker

A Python-based desktop application to track job applications, manage events, and streamline the job search process. Built with PyQt6 for the GUI and SQLite for database management.

## Features

- Add, edit, and delete job applications.
- Track events (interviews, rejections, offers, etc.) for each application.
- Filter applications by status (Pending, Active, Closed).
- User-friendly GUI built with PyQt6.

## Requirements

This project requires **Python 3.9** or later and the following packages:

- **PyQt6**: GUI framework for building the desktop application
- **PyInstaller**: Creates standalone executables from Python applications
- **pyqt6-tools**: Development tools for PyQt6 including Qt Designer
- **qt6-applications**: Additional Qt6 applications and utilities
- **pip-tools**: (Optional) For managing project dependencies

For a complete list of dependencies and their versions, see `requirements.txt`. To install all required packages, run:
```bash
pip install -r requirements.txt
```

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/job-application-tracker.git
cd job-application-tracker
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Activate the virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Step 3: Install Dependencies
Using 'requirements.txt'
```bash
pip install -r requirements.txt
```

### Step 4: Build the App
Run the following command to build the app
```bash
pyinstaller app.spec
```
The build will appear in the `dist` folder

### Step 5: Initialize the Database
The application automatically initializes the database when you first run it. Ensure the `Data` folder and the `job_tracker_template.db` file are in place.

### Project Structure
- app.py: Main entry point for the application.
- constants.py: Contains constants used throughout the project.
- UI/: Contains the GUI design files.

### License
This project is licensed under the [MIT License](LICENSE).

### Acknowledgments
- PyQt6 for the amazing GUI toolkit.
- SQLite for lightweight database management.
- PyInstaller for creating standalone executables.
