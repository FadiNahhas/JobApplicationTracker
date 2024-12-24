import constants as c 
from database import db_helper, event_manager
from table.table_helper import populate_application_table, get_selected_row_item
from helpers.button_helper import update_buttons
from helpers.filter_helper import filter_applications as apply_filter
from helpers.style_helper import load_stylesheet
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt6 import QtCore
from UI.main_window import Ui_MainWindow
from dialogs.edit_details import EditDetailsPopup
from dialogs.event_dialog import EventDialog

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
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
        # Populate the table with the applications
        populate_application_table(self.applicationTable, self.applications)

    def search_box_text_changed(self, text):
        # Filter applications based on the search text
        self.applications = db_helper.get_all_applications()
        self.applications = [app for app in self.applications if text.lower() in app.company.lower() or text.lower() in app.job_title.lower()]
        self.populate_table()

    def new_event_btn_event(self):
        # Check if an application is selected
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
        selected_row = self.eventsTable.currentRow()
        if selected_row >= 0:
            note_item = self.eventsTable.item(selected_row, 0)
            note_text = note_item.data(QtCore.Qt.ItemDataRole.UserRole + 1)

            if note_text:
                QMessageBox.information(self, "Event Note", note_text)
            else:
                self.show_warning("No Note", "No note is available for this event.")

    def delete_event_btn_event(self):
        selected_row = self.eventsTable.currentRow()  # Assuming `eventsTable` is your table widget for events.
        if selected_row < 0:
            self.show_warning("No Selection", "Please select an event to delete.")
            return
        
        event_type_item = self.eventsTable.item(selected_row, 0)  # Replace 0 with the column index of the event type.
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
            
            app_id = self.get_selected_app_id()
            app = next((app for app in self.applications if app.id == app_id), None)
            app.status = db_helper.update_application_status(app.id)
            self.refresh_application_data(app)
            self.filter_applications(self.filterMode)
            QMessageBox.information(self, "Success", "Event deleted successfully.")
        except Exception as e:
            self.show_warning("Error", f"An error occurred: {str(e)}")

    def event_row_selected_event(self):
        app_id = self.get_selected_app_id()
        app = next((app for app in self.applications if app.id == app_id), None)
        self.update_button_states(app, app_id is not None)

    def row_selected_event(self):
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
        self.companyLineEdit.setText(app.company)
        self.jobTitleLineEdit.setText(app.job_title)
        self.applyDateDateEdit.setDate(QtCore.QDate.fromString(app.application_date, "dd/MM/yyyy"))

    def reset_details_panel(self):
        self.companyLineEdit.setText("")
        self.jobTitleLineEdit.setText("")
        self.applyDateDateEdit.setDate(QtCore.QDate.currentDate())
        self.eventsTable.setRowCount(0)
        self.update_button_states()

    def new_application_btn_event(self):
        dialog = EditDetailsPopup(mode="add")
        dialog.setWindowTitle("New Application")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Extract details from dialog
            new_company = dialog.new_company_name
            new_job_title = dialog.new_job_title
            new_application_date = dialog.new_application_date.toString("dd/MM/yyyy")
            new_status = c.STATUS_PENDING

            # Insert the new application into the database
            db_helper.insert_application(new_company, new_job_title, new_application_date, new_status)

            # Refresh the application list
            self.filter_applications(self.filterMode)

    def delete_application_btn_event(self):
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

            db_helper.update_application(app.id, app.company, app.job_title, app.application_date)
            self.refresh_application_data(app)
    
    def refresh_application_data(self, app):
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
        self.filterLabel.setText(f"Filter: {filter_mode.name.title()}")
        self.filterMode = filter_mode
        all_applications = db_helper.get_all_applications()
        self.applications = apply_filter(all_applications, filter_mode)
        self.countLabel.setText(f"Applications: {len(self.applications)}")
        self.populate_table()

    def update_button_states(self, app=None, has_events=False):
        update_buttons(self, app, has_events)

    def get_selected_app_id(self):
        return get_selected_row_item(self.applicationTable, c.TABLE_COLUMN_COMPANY)
    
    def get_selected_application(self):
        app_id = self.get_selected_app_id()
        return next((app for app in self.applications if app.id == app_id), None)

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)