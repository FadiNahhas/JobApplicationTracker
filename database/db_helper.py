import sqlite3
import os
import constants as c
from models.application import Application
from models.event import Event
import requests
from constants import GOOGLE_MAPS_API_KEY

# Define the database file path
DB_PATH = os.path.join("Data", "job_tracker.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

def get_all_applications():
    """Retrieve all applications with company names and locations."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            a.id, 
            c.name, 
            a.job_title, 
            a.application_date, 
            a.status,
            l.city,
            l.latitude,
            l.longitude
        FROM applications a 
        JOIN companies c ON a.company_id = c.id
        LEFT JOIN locations l ON a.location_id = l.id
    """)
    
    applications = []
    for row in cursor.fetchall():
        app = Application(
            id=row[0],
            company=row[1],
            job_title=row[2],
            application_date=row[3],
            status=row[4],
            location=row[5],  # city from locations table
            latitude=row[6],  # latitude from locations table
            longitude=row[7]  # longitude from locations table
        )
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


def insert_application(company, job_title, apply_date, status, location=None):
    """Insert a new application into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Get or create company
        company_id = get_or_create_company(company)
        
        # Get or create location if provided
        location_id = get_or_create_location(location) if location else None
        
        cursor.execute("""
            INSERT INTO applications 
            (company_id, job_title, application_date, status, location_id) 
            VALUES (?, ?, ?, ?, ?)
        """, (company_id, job_title, apply_date, status, location_id))
        
        conn.commit()
    finally:
        conn.close()

def update_application(app_id, company, job_title, apply_date, status, location=None):
    """Update an existing application."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Get or create company
        company_id = get_or_create_company(company)
        
        # Get or create location if provided
        location_id = get_or_create_location(location) if location else None
        
        cursor.execute("""
            UPDATE applications 
            SET company_id = ?, 
                job_title = ?, 
                application_date = ?, 
                status = ?,
                location_id = ?
            WHERE id = ?
        """, (company_id, job_title, apply_date, status, location_id, app_id))
        
        conn.commit()
    finally:
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

def geocode_city(city):
    """
    Geocode city name to get coordinates using Google's Geocoding API.
    Returns (latitude, longitude) tuple.
    """
    try:
        # Construct the geocoding URL
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": city,
            "key": GOOGLE_MAPS_API_KEY
        }
        
        # Make the request
        response = requests.get(base_url, params=params)
        data = response.json()
        
        # Check if we got results
        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print(f"Geocoding failed for {city}: {data['status']}")
            return None, None
            
    except Exception as e:
        print(f"Error geocoding {city}: {str(e)}")
        return None, None

def get_or_create_location(city):
    """Get location ID or create new location using geocoding"""
    if not city:
        return None
        
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Check if location already exists
        cursor.execute("SELECT id, latitude, longitude FROM locations WHERE city = ?", (city,))
        result = cursor.fetchone()
        
        if result:
            location_id = result[0]
        else:
            # Get coordinates for new city
            lat, lng = geocode_city(city)
            if lat is not None and lng is not None:
                cursor.execute(
                    "INSERT INTO locations (city, latitude, longitude) VALUES (?, ?, ?)",
                    (city, lat, lng)
                )
                location_id = cursor.lastrowid
            else:
                location_id = None
        
        conn.commit()
        return location_id
        
    except Exception as e:
        print(f"Error in get_or_create_location: {str(e)}")
        return None
    finally:
        conn.close()
