# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmDemandsDesigner.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
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

class Ui_frmDemands(object):
    def setupUi(self, frmDemands):
        frmDemands.setObjectName(_fromUtf8("frmDemands"))
        frmDemands.resize(295, 265)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmDemands.setFont(font)
        self.centralWidget = QWidget(frmDemands)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.gridLayout = QGridLayout(self.fraTop)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblDemands = QTableWidget(self.fraTop)
        self.tblDemands.setRowCount(10)
        self.tblDemands.setObjectName(_fromUtf8("tblDemands"))
        self.tblDemands.setColumnCount(3)
        item = QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tblDemands, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
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
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmDemands.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmDemands)
        QtCore.QMetaObject.connectSlotsByName(frmDemands)

    def retranslateUi(self, frmDemands):
        frmDemands.setWindowTitle(_translate("frmDemands", "EPANET Demands Editor", None))
        item = self.tblDemands.horizontalHeaderItem(0)
        item.setText(_translate("frmDemands", "Base Demand", None))
        item = self.tblDemands.horizontalHeaderItem(1)
        item.setText(_translate("frmDemands", "Time Pattern", None))
        item = self.tblDemands.horizontalHeaderItem(2)
        item.setText(_translate("frmDemands", "Category", None))
        self.cmdOK.setText(_translate("frmDemands", "OK", None))
        self.cmdCancel.setText(_translate("frmDemands", "Cancel", None))

