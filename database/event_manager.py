from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6 import QtCore
from PyQt6.QtGui import QColor
from database import db_helper

def populate_events_table(events_table, app_id):
    events = db_helper.get_events(app_id)
    events_table.setRowCount(0)

    # Define colors for events with notes
    note_background_color = QColor("#1e282c")  # Darker background for events with notes
    note_text_color = QColor("#e5c07b")       # Soft yellow text for events with notes

    for event in events:
        row = events_table.rowCount()
        events_table.insertRow(row)

        # Create items for event type and event date
        event_type_item = QTableWidgetItem(event.event_type)
        event_type_item.setData(QtCore.Qt.ItemDataRole.UserRole, event.id)
        event_type_item.setData(QtCore.Qt.ItemDataRole.UserRole + 1, event.note)

        event_date_item = QTableWidgetItem(event.event_date)
        sortable_date = QtCore.QDate.fromString(event.event_date, "dd/MM/yyyy")
        event_date_item.setData(QtCore.Qt.ItemDataRole.UserRole, sortable_date)

        # Add note-related styling
        if event.note:
            for col in range(2):
                item = event_type_item if col == 0 else event_date_item
                item.setBackground(note_background_color)
                item.setForeground(note_text_color)  # Use soft yellow text color for contrast

        # Add items to the table
        events_table.setItem(row, 0, event_type_item)
        events_table.setItem(row, 1, event_date_item)

def add_event(app_id, event_type, event_date, note=None):
    db_helper.insert_event(app_id, event_type, event_date, note)
    return db_helper.update_application_status(app_id)

def delete_event(event_id):
    db_helper.delete_event(event_id)