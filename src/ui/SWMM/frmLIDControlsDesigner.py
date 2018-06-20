# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmLIDControlsDesigner.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_frmLIDControls(object):
    def setupUi(self, frmLIDControls):
        frmLIDControls.setObjectName(_fromUtf8("frmLIDControls"))
        frmLIDControls.resize(644, 245)
        font = QFont()
        font.setPointSize(10)
        frmLIDControls.setFont(font)
        self.centralWidget = QWidget(frmLIDControls)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QVBoxLayout(self.centralWidget)
        # self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.horizontalLayout_2 = QHBoxLayout(self.fraTop)
        # self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tblControls = QTableWidget(self.fraTop)
        self.tblControls.setObjectName(_fromUtf8("tblControls"))
        self.tblControls.setColumnCount(5)
        self.tblControls.setRowCount(0)
        item = QTableWidgetItem()
        self.tblControls.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblControls.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblControls.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tblControls.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tblControls.setHorizontalHeaderItem(4, item)
        self.horizontalLayout_2.addWidget(self.tblControls)
        self.fraButtons = QFrame(self.fraTop)
        self.fraButtons.setFrameShape(QFrame.StyledPanel)
        self.fraButtons.setFrameShadow(QFrame.Raised)
        self.fraButtons.setObjectName(_fromUtf8("fraButtons"))
        self.verticalLayout = QVBoxLayout(self.fraButtons)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnAdd = QPushButton(self.fraButtons)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.verticalLayout.addWidget(self.btnAdd)
        self.btnEdit = QPushButton(self.fraButtons)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.verticalLayout.addWidget(self.btnEdit)
        self.btnDelete = QPushButton(self.fraButtons)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.verticalLayout.addWidget(self.btnDelete)
        self.horizontalLayout_2.addWidget(self.fraButtons)
        self.verticalLayout_2.addWidget(self.fraTop)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(338, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmLIDControls.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmLIDControls)
        QtCore.QMetaObject.connectSlotsByName(frmLIDControls)

    def retranslateUi(self, frmLIDControls):
        frmLIDControls.setWindowTitle(_translate("frmLIDControls", "SWMM LID Controls", None))
        item = self.tblControls.horizontalHeaderItem(0)
        item.setText(_translate("frmLIDControls", "Control Name", None))
        item = self.tblControls.horizontalHeaderItem(1)
        item.setText(_translate("frmLIDControls", "LID Type", None))
        item = self.tblControls.horizontalHeaderItem(2)
        item.setText(_translate("frmLIDControls", "% of Area", None))
        item = self.tblControls.horizontalHeaderItem(3)
        item.setText(_translate("frmLIDControls", "% From Imperv", None))
        item = self.tblControls.horizontalHeaderItem(4)
        item.setText(_translate("frmLIDControls", "Report Flle", None))
        self.btnAdd.setText(_translate("frmLIDControls", "Add", None))
        self.btnEdit.setText(_translate("frmLIDControls", "Edit", None))
        self.btnDelete.setText(_translate("frmLIDControls", "Delete", None))
        self.cmdOK.setText(_translate("frmLIDControls", "OK", None))
        self.cmdCancel.setText(_translate("frmLIDControls", "Cancel", None))

