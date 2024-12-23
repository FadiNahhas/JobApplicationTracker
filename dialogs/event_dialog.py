from PyQt6.QtWidgets import QDialog, QMessageBox
from UI.event_dialog import Ui_new_event_dialog
from PyQt6 import QtCore

class EventDialog(QDialog, Ui_new_event_dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Default values
        self.selected_event_type = None
        self.selected_event_date = None
        self.dateDateEdit.setDate(QtCore.QDate.currentDate())

        # Connect buttons
        self.saveButton.clicked.connect(self.accept_changes)
        self.cancelButton.clicked.connect(self.reject)

    def accept_changes(self):
        self.selected_event_type = self.typeComboBox.currentText()
        self.selected_event_date = self.dateDateEdit.date()
        self.selected_event_note = self.noteTextEdit.toPlainText()

        if not self.selected_event_type:
            QMessageBox.warning(self, "Validation Error", "Please select an event type.")
            return

        self.accept()
