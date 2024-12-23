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
Using `pyinstaller` run the following command
```bash
pyinstaller app.spec
```

### Step 5: Initialize the Database
The application automatically initializes the database when you first run it. Ensure the `Data` folder and the `job_tracker_template.db` file are in place.
