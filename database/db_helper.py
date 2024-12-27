import sqlite3
import os
import constants as c
from models.application import Application
from models.event import Event

# Define the database file path
DB_PATH = os.path.join("Data", "job_tracker.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

def get_all_applications():
    """
    Retrieve all applications and their associated events from the database.
    Returns:
        List[Application]: A list of Application objects, each containing associated Event objects.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, c.name, a.job_title, a.application_date, a.status 
        FROM applications a 
        JOIN companies c ON a.company_id = c.id
    """)
    applications = []
    for row in cursor.fetchall():
        app = Application(row[0], row[1], row[2], row[3], row[4])

        # Fetch associated events
        cursor.execute("SELECT id, application_id, event_type, event_date FROM events WHERE application_id = ?", (row[0],))
        event_rows = cursor.fetchall()
        for event_row in event_rows:
            event = Event(event_row[0], event_row[1], event_row[2], event_row[3])
            app.add_event(event)

        applications.append(app)

    conn.close()
    return applications

def get_all_company_names():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM companies ORDER BY name")
    companies = [row[0] for row in cursor.fetchall()]
    conn.close()
    return companies

def get_or_create_company(company_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM companies WHERE name = ?", (company_name,))
    row = cursor.fetchone()
    if row:
        company_id = row[0]
    else:
        cursor.execute("INSERT INTO companies (name) VALUES (?)", (company_name,))
        # Get ID using SELECT last_insert_rowid()
        cursor.execute("SELECT last_insert_rowid()")
        company_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return company_id


def insert_application(company, job_title, apply_date, status):
    """
    Insert a new application into the database.
    Args:
        company (str): The company name.
        job_title (str): The job title.
        apply_date (str): The application date.
        status (str): The application status.
    """
    conn = connect_db()
    cursor = conn.cursor()
    company_id = get_or_create_company(company)

    cursor.execute("INSERT INTO applications (company_id, job_title, application_date, status) VALUES (?, ?, ?, ?)",
                   (company_id, job_title, apply_date, status))
    conn.commit()
    conn.close()

def update_application(app_id, company, job_title, apply_date):
    """
    Update an application in the database.
    Args:
        app_id (int): The application ID.
        company (str): The company name.
        job_title (str): The job title.
        apply_date (str): The application date.
    """
    conn = connect_db()
    cursor = conn.cursor()
    company_id = get_or_create_company(company)

    cursor.execute("UPDATE applications SET company_id = ?, job_title = ?, application_date = ? WHERE id = ?",
                   (company_id, job_title, apply_date, app_id))
    conn.commit()
    conn.close()

def delete_application(app_id):
    """
    Delete an application and its associated events from the database.
    Args:
        app_id (int): The application ID.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events WHERE application_id = ?", (app_id,))
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()

def get_events(app_id):
    """
    Retrieve all events associated with a given application ID.
    Args:
        app_id (int): The application ID.
    Returns:
        List[Event]: A list of Event objects.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, application_id, event_type, event_date, note FROM events WHERE application_id = ?", (app_id,))
    rows = cursor.fetchall()

    events = [Event(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    conn.close()
    return events

def insert_event(app_id, event_type, event_date, note=None):
    """
    Insert a new event into the database.
    Args:
        app_id (int): The application ID.
        event_type (str): The event type.
        event_date (str): The event date.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO events (application_id, event_type, event_date, note) VALUES (?, ?, ?, ?)",
                   (app_id, event_type, event_date, note))
    conn.commit()
    conn.close()

def delete_event(event_id):
    """
    Delete an event from the database.
    Args:
        event_id (int): The event ID.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def update_application_status(app_id):
    """
    Update the status of an application based on the latest event date.
    Args:
        app_id (int): The application ID.
    Returns:
        str: The updated application status.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch associated events
    cursor.execute("SELECT event_type FROM events WHERE application_id = ?", (app_id,))
    events = [event[0] for event in cursor.fetchall()]

    # Determine new status
    if not events:
        new_status = c.STATUS_PENDING
    elif "Rejection" in events:
        new_status = c.STATUS_CLOSED
    else:
        new_status = c.STATUS_ACTIVE

    # Update status in the database
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()
    return new_status
