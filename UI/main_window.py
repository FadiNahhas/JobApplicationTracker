# Form implementation generated from reading ui file 'UI/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(927, 602)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.navbarColumn = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navbarColumn.sizePolicy().hasHeightForWidth())
        self.navbarColumn.setSizePolicy(sizePolicy)
        self.navbarColumn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.navbarColumn.setAutoFillBackground(False)
        self.navbarColumn.setObjectName("navbarColumn")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.navbarColumn)
        self.verticalLayout_2.setContentsMargins(12, 12, 12, 12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_0 = QtWidgets.QPushButton(parent=self.navbarColumn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_0.sizePolicy().hasHeightForWidth())
        self.btn_0.setSizePolicy(sizePolicy)
        self.btn_0.setObjectName("btn_0")
        self.verticalLayout_2.addWidget(self.btn_0)
        self.btn_2 = QtWidgets.QPushButton(parent=self.navbarColumn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_2.sizePolicy().hasHeightForWidth())
        self.btn_2.setSizePolicy(sizePolicy)
        self.btn_2.setObjectName("btn_2")
        self.verticalLayout_2.addWidget(self.btn_2)
        self.btn_1 = QtWidgets.QPushButton(parent=self.navbarColumn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_1.sizePolicy().hasHeightForWidth())
        self.btn_1.setSizePolicy(sizePolicy)
        self.btn_1.setObjectName("btn_1")
        self.verticalLayout_2.addWidget(self.btn_1)
        self.line = QtWidgets.QFrame(parent=self.navbarColumn)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.newApplicationButton = QtWidgets.QPushButton(parent=self.navbarColumn)
        self.newApplicationButton.setObjectName("newApplicationButton")
        self.verticalLayout_2.addWidget(self.newApplicationButton)
        self.deleteApplicationButton = QtWidgets.QPushButton(parent=self.navbarColumn)
        self.deleteApplicationButton.setObjectName("deleteApplicationButton")
        self.verticalLayout_2.addWidget(self.deleteApplicationButton)
        self.line_2 = QtWidgets.QFrame(parent=self.navbarColumn)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.mapButton = QtWidgets.QPushButton(parent=self.navbarColumn)
        self.mapButton.setObjectName("mapButton")
        self.verticalLayout_2.addWidget(self.mapButton)
        self.horizontalLayout_2.addWidget(self.navbarColumn, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.tableColumn = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableColumn.sizePolicy().hasHeightForWidth())
        self.tableColumn.setSizePolicy(sizePolicy)
        self.tableColumn.setObjectName("tableColumn")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tableColumn)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.searchBox = QtWidgets.QLineEdit(parent=self.tableColumn)
        self.searchBox.setObjectName("searchBox")
        self.verticalLayout_3.addWidget(self.searchBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filterLabel = QtWidgets.QLabel(parent=self.tableColumn)
        self.filterLabel.setObjectName("filterLabel")
        self.horizontalLayout.addWidget(self.filterLabel)
        self.countLabel = QtWidgets.QLabel(parent=self.tableColumn)
        self.countLabel.setObjectName("countLabel")
        self.horizontalLayout.addWidget(self.countLabel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.applicationTable = QtWidgets.QTableWidget(parent=self.tableColumn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applicationTable.sizePolicy().hasHeightForWidth())
        self.applicationTable.setSizePolicy(sizePolicy)
        self.applicationTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.applicationTable.setAlternatingRowColors(True)
        self.applicationTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.applicationTable.setColumnCount(4)
        self.applicationTable.setObjectName("applicationTable")
        self.applicationTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.applicationTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.applicationTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.applicationTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.applicationTable.setHorizontalHeaderItem(3, item)
        self.applicationTable.horizontalHeader().setCascadingSectionResizes(False)
        self.applicationTable.horizontalHeader().setStretchLastSection(True)
        self.applicationTable.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.applicationTable)
        self.horizontalLayout_2.addWidget(self.tableColumn)
        self.detailsColumn = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detailsColumn.sizePolicy().hasHeightForWidth())
        self.detailsColumn.setSizePolicy(sizePolicy)
        self.detailsColumn.setObjectName("detailsColumn")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.detailsColumn)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.detailsForm = QtWidgets.QFormLayout()
        self.detailsForm.setObjectName("detailsForm")
        self.companyLabel = QtWidgets.QLabel(parent=self.detailsColumn)
        self.companyLabel.setObjectName("companyLabel")
        self.detailsForm.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.companyLabel)
        self.companyLineEdit = QtWidgets.QLineEdit(parent=self.detailsColumn)
        self.companyLineEdit.setReadOnly(True)
        self.companyLineEdit.setObjectName("companyLineEdit")
        self.detailsForm.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.companyLineEdit)
        self.jobTitleLabel = QtWidgets.QLabel(parent=self.detailsColumn)
        self.jobTitleLabel.setObjectName("jobTitleLabel")
        self.detailsForm.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.jobTitleLabel)
        self.jobTitleLineEdit = QtWidgets.QLineEdit(parent=self.detailsColumn)
        self.jobTitleLineEdit.setReadOnly(True)
        self.jobTitleLineEdit.setObjectName("jobTitleLineEdit")
        self.detailsForm.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.jobTitleLineEdit)
        self.applyDateLabel = QtWidgets.QLabel(parent=self.detailsColumn)
        self.applyDateLabel.setObjectName("applyDateLabel")
        self.detailsForm.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.applyDateLabel)
        self.applyDateDateEdit = QtWidgets.QDateEdit(parent=self.detailsColumn)
        self.applyDateDateEdit.setFrame(True)
        self.applyDateDateEdit.setReadOnly(True)
        self.applyDateDateEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.applyDateDateEdit.setObjectName("applyDateDateEdit")
        self.detailsForm.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.applyDateDateEdit)
        self.locationLabel = QtWidgets.QLabel(parent=self.detailsColumn)
        self.locationLabel.setObjectName("locationLabel")
        self.detailsForm.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.locationLabel)
        self.locationLineEdit = QtWidgets.QLineEdit(parent=self.detailsColumn)
        self.locationLineEdit.setReadOnly(True)
        self.locationLineEdit.setObjectName("locationLineEdit")
        self.detailsForm.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.locationLineEdit)
        self.verticalLayout_4.addLayout(self.detailsForm)
        self.editButton = QtWidgets.QPushButton(parent=self.detailsColumn)
        self.editButton.setObjectName("editButton")
        self.verticalLayout_4.addWidget(self.editButton)
        self.eventsPanel = QtWidgets.QGroupBox(parent=self.detailsColumn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eventsPanel.sizePolicy().hasHeightForWidth())
        self.eventsPanel.setSizePolicy(sizePolicy)
        self.eventsPanel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.eventsPanel.setObjectName("eventsPanel")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.eventsPanel)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.eventsTable = QtWidgets.QTableWidget(parent=self.eventsPanel)
        self.eventsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.eventsTable.setAlternatingRowColors(False)
        self.eventsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.eventsTable.setColumnCount(2)
        self.eventsTable.setObjectName("eventsTable")
        self.eventsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(1, item)
        self.eventsTable.horizontalHeader().setStretchLastSection(True)
        self.eventsTable.verticalHeader().setVisible(False)
        self.verticalLayout_5.addWidget(self.eventsTable)
        self.eventButtons = QtWidgets.QHBoxLayout()
        self.eventButtons.setObjectName("eventButtons")
        self.deleteEventButton = QtWidgets.QPushButton(parent=self.eventsPanel)
        self.deleteEventButton.setStyleSheet("")
        self.deleteEventButton.setObjectName("deleteEventButton")
        self.eventButtons.addWidget(self.deleteEventButton)
        self.newEventButton = QtWidgets.QPushButton(parent=self.eventsPanel)
        self.newEventButton.setObjectName("newEventButton")
        self.eventButtons.addWidget(self.newEventButton)
        self.viewNoteButton = QtWidgets.QPushButton(parent=self.eventsPanel)
        self.viewNoteButton.setObjectName("viewNoteButton")
        self.eventButtons.addWidget(self.viewNoteButton)
        self.verticalLayout_5.addLayout(self.eventButtons)
        self.verticalLayout_4.addWidget(self.eventsPanel)
        self.horizontalLayout_2.addWidget(self.detailsColumn)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Job Application Tracker"))
        self.btn_0.setText(_translate("MainWindow", "All"))
        self.btn_2.setText(_translate("MainWindow", "Open"))
        self.btn_1.setText(_translate("MainWindow", "Closed"))
        self.newApplicationButton.setText(_translate("MainWindow", "New"))
        self.deleteApplicationButton.setText(_translate("MainWindow", "Delete"))
        self.mapButton.setText(_translate("MainWindow", "Map"))
        self.searchBox.setPlaceholderText(_translate("MainWindow", "Search"))
        self.filterLabel.setText(_translate("MainWindow", "Filter:"))
        self.countLabel.setText(_translate("MainWindow", "Applications:"))
        self.applicationTable.setSortingEnabled(False)
        item = self.applicationTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Company"))
        item = self.applicationTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Job Title"))
        item = self.applicationTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Apply Date"))
        item = self.applicationTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        self.companyLabel.setText(_translate("MainWindow", "Company"))
        self.jobTitleLabel.setText(_translate("MainWindow", "Job Title"))
        self.applyDateLabel.setText(_translate("MainWindow", "Apply Date"))
        self.applyDateDateEdit.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy"))
        self.locationLabel.setText(_translate("MainWindow", "Location"))
        self.editButton.setText(_translate("MainWindow", "Edit"))
        self.eventsPanel.setTitle(_translate("MainWindow", "Events"))
        self.eventsTable.setSortingEnabled(False)
        item = self.eventsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Type"))
        item = self.eventsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Date"))
        self.deleteEventButton.setText(_translate("MainWindow", "Delete Event"))
        self.newEventButton.setText(_translate("MainWindow", "New Event"))
        self.viewNoteButton.setText(_translate("MainWindow", "View Note"))
