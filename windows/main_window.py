"""
Job Application Tracker - Main Window Module

This module implements the main application window and its core functionality.
It handles user interactions, data display, and manages the application's primary features.

Classes:
    MainWindow: The primary window of the application, inheriting from QMainWindow

Features:
- Application management (add/edit/delete)
- Event tracking
- Status filtering
- Search functionality
- Map visualization
- Details panel management
"""
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt6 import QtCore
from UI.main_window import Ui_MainWindow
from dialogs.edit_details import EditDetailsPopup
from dialogs.event_dialog import EventDialog
import constants as c 
from database import db_helper, event_manager
from models.application import Application
from table.table_helper import populate_application_table, get_selected_row_item
from helpers.button_helper import update_buttons
from helpers.filter_helper import filter_applications as apply_filter

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main application window handling user interactions and data display.

    Attributes:
        applications (list): List of Application objects
        filterMode (FilterMode): Current filter mode for applications
        events (list): List of Event objects for selected application
    """
    def __init__(self):
        """Initialize the main window and set up UI elements."""
        super().__init__()
        self.setupUi(self)

        # Connect filter buttons
        self.btn_0.clicked.connect(lambda: self.filter_applications(c.FilterMode.ALL))
        self.btn_1.clicked.connect(lambda: self.filter_applications(c.FilterMode.CLOSED))
        self.btn_2.clicked.connect(lambda: self.filter_applications(c.FilterMode.ACTIVE))

        # Connect application buttons
        self.editButton.clicked.connect(self.edit_details_btn_event)
        self.newApplicationButton.clicked.connect(self.new_application_btn_event)
        self.deleteApplicationButton.clicked.connect(self.delete_application_btn_event)

        # Connect map buttons
        self.mapButton.clicked.connect(self.map_btn_event)

        # Connect event buttons
        self.newEventButton.clicked.connect(self.new_event_btn_event)
        self.deleteEventButton.clicked.connect(self.delete_event_btn_event)
        self.viewNoteButton.clicked.connect(self.view_note_btn_event)

        # Connect search box
        self.searchBox.textChanged.connect(self.search_box_text_changed)

        # Connect table events
        self.applicationTable.itemSelectionChanged.connect(self.row_selected_event)
        self.eventsTable.itemSelectionChanged.connect(self.event_row_selected_event)

        # Set initial button states
        self.update_button_states()

        # Initialize table data
        self.applications = db_helper.get_all_applications()
        # Set default filter mode and populate table
        self.filter_applications(c.FilterMode.ALL)
        self.events = []
    
    def populate_table(self):
        """Populate the applications table with current data."""
        populate_application_table(self.applicationTable, self.applications)

    def search_box_text_changed(self, text):
        """
        Filter applications based on search text.
        
        Args:
            text (str): Search query text
        """
        self.applications = db_helper.get_all_applications()
        self.applications = [app for app in self.applications
                            if text.lower() in app.company.lower()
                            or text.lower() in app.job_title.lower()]
        self.populate_table()

    def map_btn_event(self):
        """Open the map dialog showing application locations."""
        from dialogs.map_dialog import MapDialog
        dialog = MapDialog(self.applications)
        dialog.exec()

    def new_event_btn_event(self):
        """Handle creation of new events for selected application."""
        selected_row = self.applicationTable.currentRow()
        if selected_row < 0:
            self.show_warning("No Selection", "Please select an application to add an event.")
            return
        
        # Find the application object from the list
        app = app = self.get_selected_application()
        if not app:
            self.show_warning("Error", "Could not determine the selected application.")
            return

        # Open the event dialog
        dialog = EventDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_event_type = dialog.selected_event_type
            new_event_date = dialog.selected_event_date.toString("dd/MM/yyyy")
            new_event_note = dialog.selected_event_note

            if not new_event_type or not new_event_date:
                self.show_warning("Error", "Please select an event type and date.")
                return

            try:
                # Add the event to the database and update the application status
                event_manager.add_event(app.id, new_event_type, new_event_date, new_event_note)
                new_status = db_helper.update_application_status(app.id)
                app.status = new_status
                self.refresh_application_data(app)
                self.filter_applications(self.filterMode)

                QMessageBox.information(self, "Success", "Event added successfully.")
            
            except Exception as e:
                self.show_warning("Error", f"An error occurred: {str(e)}")

    def view_note_btn_event(self):
        """
        Display the note associated with the selected event in a message box.
        
        This method is triggered when the view note button is clicked. It retrieves
        the note text stored in the UserRole+1 data of the first column of the selected
        event row and displays it in a QMessageBox. If no note exists, displays a
        warning message.

        The note text is stored as custom data in the table item using Qt's UserRole+1
        to avoid interfering with the default roles (DisplayRole, UserRole).

        Returns:
            None
        """
        selected_row = self.eventsTable.currentRow()
        if selected_row >= 0:
            note_item = self.eventsTable.item(selected_row, 0)
            note_text = note_item.data(QtCore.Qt.ItemDataRole.UserRole + 1)

            if note_text:
                QMessageBox.information(self, "Event Note", note_text)
            else:
                self.show_warning("No Note", "No note is available for this event.")

    def delete_event_btn_event(self):
        """
        Handle the deletion of an event from the selected application.

        This method is triggered when the delete event button is clicked. It performs the following steps:
        1. Validates that an event is selected in the events table
        2. Retrieves the event ID from the table item's UserRole data
        3. Prompts for user confirmation before deletion
        4. Deletes the event from the database
        5. Updates the application's status
        6. Refreshes the UI to reflect changes

        The method includes error handling for:
        - No event selected
        - Invalid event data
        - Database operation failures

        Returns:
            None
        """
        selected_row = self.eventsTable.currentRow()
        if selected_row < 0:
            self.show_warning("No Selection", "Please select an event to delete.")
            return
        
        event_type_item = self.eventsTable.item(selected_row, 0)
        if event_type_item is None:
            self.show_warning("Error", "Could not determine the selected event.")
            return

        event_id = event_type_item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not event_id:
            self.show_warning("Error", "Could not determine the selected event.")
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this event?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.No:
            return

        try:
            event_manager.delete_event(event_id)
            selected_row = self.applicationTable.currentRow()
            if selected_row < 0:
                self.show_warning("No Selection", "Please select an application to delete.")
                return
            
            app = self.get_selected_application()
            app.status = db_helper.update_application_status(app.id)
            self.refresh_application_data(app)
            self.filter_applications(self.filterMode)
            QMessageBox.information(self, "Success", "Event deleted successfully.")
        except Exception as e:
            self.show_warning("Error", f"An error occurred: {str(e)}")

    def event_row_selected_event(self):
        """
        Handle the selection of an event row in the events table.

        This method is triggered whenever a row in the events table is selected.
        It updates the button states based on the currently selected application
        and whether any events exist.

        Process:
        1. Gets the ID of the currently selected application
        2. Finds the corresponding application object from the applications list
        3. Updates the UI button states based on the application and event selection

        Returns:
            None
        """
        app_id = self.get_selected_app_id()
        app = next((app for app in self.applications if app.id == app_id), None)
        self.update_button_states(app, app_id is not None)

    def row_selected_event(self):
        """
        Handle the selection of a row in the applications table.

        This method is triggered when a user selects a row in the main applications table.
        It updates the UI to display the selected application's details and related events.

        Process:
        1. Checks if any items are selected in the applications table
        2. If selected:
           - Retrieves the application data for the selected row
           - Updates the details panel with application information
           - Updates button states based on application and event data
           - Populates the events table with related events
        3. If no selection:
           - Disables relevant buttons
           - Resets the details panel to default state

        Note:
            Uses the TABLE_COLUMN_COMPANY constant from constants.py to identify
            the correct column for the application ID.
        """
        select_items = self.applicationTable.selectedItems()

        if select_items:
            selected_row = self.applicationTable.currentRow()
            if selected_row >= 0:
                app_id_item = self.applicationTable.item(selected_row, c.TABLE_COLUMN_COMPANY)
                if app_id_item:
                    app = self.get_selected_application()
                    if app:
                        self.update_details_panel(app)
                        self.update_button_states(app, len(db_helper.get_events(app.id)) > 0)
                        event_manager.populate_events_table(self.eventsTable, app.id)
                    else:
                        print("Could not find application with ID", app.id)
        else:
            self.update_button_states()
            self.reset_details_panel()

    def update_details_panel(self, app):
        """
        Update the details panel with information from the selected application.

        This method populates the detail panel's input fields with data from
        the provided application object.

        Args:
            app: Application object containing the following attributes:
                - company: String name of the company
                - job_title: String title of the position
                - application_date: String date in format "dd/MM/yyyy"
                - location: String location (can be None)

        Note:
            The date string is converted to a QDate object for the date edit field.
            Empty location values are displayed as empty strings.
        """
        self.companyLineEdit.setText(app.company)
        self.jobTitleLineEdit.setText(app.job_title)
        self.applyDateDateEdit.setDate(QtCore.QDate.fromString(app.application_date, "dd/MM/yyyy"))
        self.locationLineEdit.setText(app.location if app.location else "")

    def reset_details_panel(self):
        """
        Reset the details panel to its default state.

        This method clears all input fields in the details panel and sets them
        to their default values:
        - Empty strings for text fields
        - Current date for the date field
        - Clears the events table
        - Updates button states to reflect no selection

        Called when:
        - No application is selected
        - After deleting an application
        - When clearing the selection
        """
        self.companyLineEdit.setText("")
        self.jobTitleLineEdit.setText("")
        self.applyDateDateEdit.setDate(QtCore.QDate.currentDate())
        self.locationLineEdit.setText("")
        self.eventsTable.setRowCount(0)
        self.update_button_states()

    def new_application_btn_event(self):
        """
        Handle the creation of a new job application.

        This method is triggered when the new application button is clicked.
        It opens a dialog for entering new application details and processes
        the input if accepted.

        Process:
        1. Opens the EditDetailsPopup dialog in "add" mode
        2. If user accepts the dialog:
           - Extracts the entered details (company, job title, date, location)
           - Sets initial status as PENDING
           - Inserts the new application into the database
           - Refreshes the application list with current filter

        Note:
            - Application date is converted to string format "dd/MM/yyyy"
            - Initial status is set using constant STATUS_PENDING from constants.py
            - The application list is refreshed maintaining the current filter mode
        """
        dialog = EditDetailsPopup(mode="add")
        dialog.setWindowTitle("New Application")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Extract details from dialog
            new_company = dialog.new_company_name
            new_job_title = dialog.new_job_title
            new_application_date = dialog.new_application_date.toString("dd/MM/yyyy")
            new_status = c.STATUS_PENDING
            new_location = dialog.new_location

            # Insert the new application into the database
            db_helper.insert_application(new_company, new_job_title, new_application_date, new_status, new_location)

            # Refresh the application list
            self.filter_applications(self.filterMode)

    def delete_application_btn_event(self):
        """
        Handle the deletion of a job application.

        This method is triggered when the delete application button is clicked.
        It verifies the selection, asks for confirmation, and handles the deletion
        process.

        Process:
        1. Validates that an application is selected
        2. Gets the application ID and verifies it exists
        3. Shows a confirmation dialog
        4. If confirmed:
           - Deletes the application from the database
           - Refreshes the application list
           - Resets the details panel
           - Clears the selection

        Note:
            Shows warning messages if:
            - No application is selected
            - Cannot determine the selected application
        """
        selected_row = self.applicationTable.currentRow()
        if selected_row < 0:
            self.show_warning("No Selection", "Please select an application to delete.")
            return
        
        app_id = self.get_selected_app_id()
        if not app_id:
            self.show_warning("Error", "Could not determine the selected application.")
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.No:
            return
        
        db_helper.delete_application(app_id)

        self.filter_applications(self.filterMode)
        self.reset_details_panel()
        self.applicationTable.clearSelection()

    def edit_details_btn_event(self):
        """
        Handle editing of an existing job application's details.

        This method is triggered when the edit details button is clicked.
        It opens a dialog pre-populated with the current application details
        and processes any changes if accepted.

        Process:
        1. Validates that an application is selected
        2. Gets the selected application object
        3. Opens EditDetailsPopup dialog with current application data
        4. If changes are accepted:
           - Updates application object with new values
           - Saves changes to database
           - Refreshes the application display

        Args handled by dialog:
            - company: Company name
            - job_title: Position title
            - application_date: Application date (formatted as "dd/MM/yyyy")
            - location: Job location

        Note:
            Silently returns if no application is selected
        """
        selected_row = self.applicationTable.currentRow()
        if selected_row < 0:
            return
        
        app = self.get_selected_application()

        dialog = EditDetailsPopup(app)
        dialog.setWindowTitle("Edit Details")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            app.company = dialog.new_company_name
            app.job_title = dialog.new_job_title
            app.application_date = dialog.new_application_date.toString("dd/MM/yyyy")
            app.location = dialog.new_location
            db_helper.update_application(app.id, app.company, app.job_title, app.application_date, app.status, app.location)
            self.refresh_application_data(app)
    
    def refresh_application_data(self, app):
        """
        Refresh the application table and maintain selection.

        This method updates the application list from the database,
        repopulates the table, and maintains the selection on the specified
        application.

        Args:
            app: Application object whose selection should be maintained after refresh

        Process:
        1. Reloads all applications from database
        2. Repopulates the table
        3. Finds and selects the specified application in the table
        4. Updates the events table for the selected application
        """
        self.applications = db_helper.get_all_applications()
        self.populate_table()

        row_count = self.applicationTable.rowCount()
        for row in range(row_count):
            item = self.applicationTable.item(row, c.TABLE_COLUMN_COMPANY)
            if not item:
                continue
            table_app_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
            if table_app_id == app.id:
                self.applicationTable.selectRow(row)
                break

        event_manager.populate_events_table(self.eventsTable, app.id)

    def filter_applications(self, filter_mode):
        """
        Filter and display applications based on the specified mode.

        Args:
            filter_mode: FilterMode enum value specifying the filter to apply

        Updates:
        - Filter label with current mode
        - Applications list with filtered results
        - Count label with number of filtered applications
        - Table contents with filtered applications
        """
        self.filterLabel.setText(f"Filter: {filter_mode.name.title()}")
        self.filterMode = filter_mode
        all_applications = db_helper.get_all_applications()
        self.applications = apply_filter(all_applications, filter_mode)
        self.countLabel.setText(f"Applications: {len(self.applications)}")
        self.populate_table()

    def update_button_states(self, app=None, has_events=False):
        """
        Update the enabled/disabled states of UI buttons.

        Args:
            app: Optional Application object. If None, disables application-specific buttons
            has_events: Boolean indicating if the application has associated events
        """
        update_buttons(self, app, has_events)

    def get_selected_app_id(self):
        """
        Get the ID of the currently selected application.

        Returns:
            int: The ID of the selected application, or None if no selection
        """
        return get_selected_row_item(self.applicationTable, c.TABLE_COLUMN_COMPANY)
    
    def get_selected_application(self) -> Application:
        """
        Get the Application object for the currently selected row.

        Returns:
            Application: The selected application object

        Raises:
            ValueError: If no application is selected
        """
        app_id = self.get_selected_app_id()
        app = next((app for app in self.applications if app.id == app_id), None)
        if app is None:
            raise ValueError("No application selected")
        return app

    def show_warning(self, title, message):
        """
        Display a warning message dialog.

        Args:
            title: String title for the warning dialog
            message: String message to display in the dialog
        """
        QMessageBox.warning(self, title, message)