# Form implementation generated from reading ui file 'UI/map_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_mapDialog(object):
    def setupUi(self, mapDialog):
        mapDialog.setObjectName("mapDialog")
        mapDialog.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(mapDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mapLayout = QtWidgets.QVBoxLayout()
        self.mapLayout.setObjectName("mapLayout")
        self.verticalLayout.addLayout(self.mapLayout)

        self.retranslateUi(mapDialog)
        QtCore.QMetaObject.connectSlotsByName(mapDialog)

    def retranslateUi(self, mapDialog):
        _translate = QtCore.QCoreApplication.translate
        mapDialog.setWindowTitle(_translate("mapDialog", "Map"))