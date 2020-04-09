# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui-py3qt5\src\ui\SWMM\frmDetailsDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmDetails(object):
    def setupUi(self, frmDetails):
        frmDetails.setObjectName("frmDetails")
        frmDetails.resize(541, 405)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmDetails.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmDetails)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gbxCategory = QtWidgets.QGroupBox(self.centralWidget)
        self.gbxCategory.setMaximumSize(QtCore.QSize(200, 16777215))
        self.gbxCategory.setObjectName("gbxCategory")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gbxCategory)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lstCategory = QtWidgets.QListWidget(self.gbxCategory)
        self.lstCategory.setObjectName("lstCategory")
        self.verticalLayout_3.addWidget(self.lstCategory)
        self.horizontalLayout.addWidget(self.gbxCategory)
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tableWidget)
        frmDetails.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmDetails)
        QtCore.QMetaObject.connectSlotsByName(frmDetails)

    def retranslateUi(self, frmDetails):
        _translate = QtCore.QCoreApplication.translate
        frmDetails.setWindowTitle(_translate("frmDetails", "SWMM Project Details"))
        self.gbxCategory.setTitle(_translate("frmDetails", "Data Category"))

