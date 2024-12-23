from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6 import QtCore, QtGui
import constants as c

def create_table_item(text, data=None):
    # Create a QTableWidgetItem with the given text and data
    item = QTableWidgetItem(text)
    if data:
        item.setData(QtCore.Qt.ItemDataRole.UserRole, data)
    return item

def get_selected_row_item(table, column):
    selected_row = table.currentRow()
    if selected_row < 0:
        return None
    
    item = table.item(selected_row, column)
    return item.data(QtCore.Qt.ItemDataRole.UserRole) if item else None

def populate_application_table(table, applications):
    # Populate the given QTableWidget with the given applications
    table.setRowCount(0)
    applications = list(applications)
    applications.sort(key=lambda app: QtCore.QDate.fromString(app.application_date, "dd/MM/yyyy"), reverse=True)

    for app in applications:
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, c.TABLE_COLUMN_COMPANY, create_table_item(app.company, app.id))
        table.setItem(row, c.TABLE_COLUMN_JOB_TITLE, create_table_item(app.job_title))
        sortable_date = QtCore.QDate.fromString(app.application_date, "dd/MM/yyyy")
        table.setItem(row, c.TABLE_COLUMN_DATE_APPLIED, create_table_item(app.application_date, sortable_date))

        # Create and style status item
        status_item = create_table_item(app.status)
        if app.status == c.STATUS_PENDING:
            status_item.setBackground(QtGui.QColor(255, 255, 0, 50))
        elif app.status == c.STATUS_CLOSED:
            status_item.setBackground(QtGui.QColor(255, 0, 0, 50))
        elif app.status == c.STATUS_ACTIVE:
            status_item.setBackground(QtGui.QColor(0, 255, 0, 50))
        table.setItem(row, c.TABLE_COLUMN_STATUS, status_item)