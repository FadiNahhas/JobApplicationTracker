from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import QtCore
from UI.edit_dialog import Ui_editDetailsPopup

class EditDetailsPopup(QDialog, Ui_editDetailsPopup):
    def __init__(self, app=None, mode="edit"):
        super().__init__()
        self.setupUi(self)

        if mode == "edit" and app:
            self.companyLineEdit.setText(app.company)
            self.jobTitleLineEdit.setText(app.job_title)
            self.applyDateDateEdit.setDate(QtCore.QDate.fromString(app.application_date, "dd/MM/yyyy"))
        else:
            self.companyLineEdit.setText("")
            self.jobTitleLineEdit.setText("")
            self.applyDateDateEdit.setDate(QtCore.QDate.currentDate())

        self.new_company_name = None
        self.new_job_title = None
        self.new_application_date = None

        self.saveButton.clicked.connect(self.accept_changes)
        self.cancelButton.clicked.connect(self.reject)

    def accept_changes(self):
        company_name = self.companyLineEdit.text().strip()
        job_title = self.jobTitleLineEdit.text().strip()

        if not company_name or not job_title:
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        self.new_company_name = company_name
        self.new_job_title = job_title
        self.new_application_date = self.applyDateDateEdit.date()
        self.accept()
