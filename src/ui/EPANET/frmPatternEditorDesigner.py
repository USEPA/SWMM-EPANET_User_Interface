# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmPatternEditorDesigner.ui'
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

class Ui_frmPatternEditor(object):
    def setupUi(self, frmPatternEditor):
        frmPatternEditor.setObjectName(_fromUtf8("frmPatternEditor"))
        frmPatternEditor.resize(575, 221)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmPatternEditor.setFont(font)
        self.centralWidget = QWidget(frmPatternEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraParms = QFrame(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraParms.sizePolicy().hasHeightForWidth())
        self.fraParms.setSizePolicy(sizePolicy)
        self.fraParms.setFrameShape(QFrame.StyledPanel)
        self.fraParms.setFrameShadow(QFrame.Raised)
        self.fraParms.setObjectName(_fromUtf8("fraParms"))
        self.gridLayout = QGridLayout(self.fraParms)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QSpacerItem(325, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblDescription = QLabel(self.fraParms)
        self.lblDescription.setObjectName(_fromUtf8("lblDescription"))
        self.gridLayout.addWidget(self.lblDescription, 1, 0, 1, 1)
        self.lblPatternID = QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblPatternID.setFont(font)
        self.lblPatternID.setObjectName(_fromUtf8("lblPatternID"))
        self.gridLayout.addWidget(self.lblPatternID, 0, 0, 1, 1)
        self.tblMult = QTableWidget(self.fraParms)
        self.tblMult.setRowCount(1)
        self.tblMult.setColumnCount(24)
        self.tblMult.setObjectName(_fromUtf8("tblMult"))
        item = QTableWidgetItem()
        self.tblMult.setVerticalHeaderItem(0, item)
        self.gridLayout.addWidget(self.tblMult, 2, 0, 1, 3)
        self.txtPatternID = QLineEdit(self.fraParms)
        self.txtPatternID.setObjectName(_fromUtf8("txtPatternID"))
        self.gridLayout.addWidget(self.txtPatternID, 0, 1, 1, 1)
        self.txtDescription = QLineEdit(self.fraParms)
        self.txtDescription.setObjectName(_fromUtf8("txtDescription"))
        self.gridLayout.addWidget(self.txtDescription, 1, 1, 1, 2)
        self.verticalLayout.addWidget(self.fraParms)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QSpacerItem(99, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmPatternEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmPatternEditor)
        QtCore.QMetaObject.connectSlotsByName(frmPatternEditor)

    def retranslateUi(self, frmPatternEditor):
        frmPatternEditor.setWindowTitle(_translate("frmPatternEditor", "EPANET Pattern Editor", None))
        self.lblDescription.setText(_translate("frmPatternEditor", "<html><head/><body><p>Description</p></body></html>", None))
        self.lblPatternID.setText(_translate("frmPatternEditor", "Pattern ID", None))
        item = self.tblMult.verticalHeaderItem(0)
        item.setText(_translate("frmPatternEditor", "Multiplier", None))
        self.cmdOK.setText(_translate("frmPatternEditor", "OK", None))
        self.cmdCancel.setText(_translate("frmPatternEditor", "Cancel", None))

