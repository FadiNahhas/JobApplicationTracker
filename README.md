# Job Application Tracker

A Python-based desktop application to track job applications, manage events, and streamline the job search process. Built with PyQt6 for the GUI and SQLite for database management.

## Features

- Add, edit, and delete job applications.
- Track events (interviews, rejections, offers, etc.) for each application.
- Filter applications by status (Pending, Active, Closed).
- User-friendly GUI built with PyQt6.

## Requirements

This project is compatible with **Python 3.9** or later. The following Python libraries are required:

- **PyQt6**: For the graphical user interface.
- **PyInstaller**: For building the application as an executable.
- **pyqt6-tools**: Provides tools like Designer and Linguist for PyQt6 development.
- **qt6-applications**: Includes additional Qt6-based applications and tools.

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
