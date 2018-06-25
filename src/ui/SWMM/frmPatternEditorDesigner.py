# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmPatternEditorDesigner.ui'
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

class Ui_frmPatternEditor(object):
    def setupUi(self, frmPatternEditor):
        frmPatternEditor.setObjectName(_fromUtf8("frmPatternEditor"))
        frmPatternEditor.resize(606, 319)
        font = QFont()
        font.setPointSize(10)
        frmPatternEditor.setFont(font)
        self.centralWidget = QWidget(frmPatternEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QVBoxLayout(self.centralWidget)
        # self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraParms = QFrame(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
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
        self.lblPatternID = QLabel(self.fraParms)
        font = QFont()
        font.setPointSize(10)
        self.lblPatternID.setFont(font)
        self.lblPatternID.setObjectName(_fromUtf8("lblPatternID"))
        self.gridLayout.addWidget(self.lblPatternID, 0, 0, 1, 1)
        self.txtPatternID = QLineEdit(self.fraParms)
        self.txtPatternID.setObjectName(_fromUtf8("txtPatternID"))
        self.gridLayout.addWidget(self.txtPatternID, 0, 1, 1, 1)
        self.lblType = QLabel(self.fraParms)
        font = QFont()
        font.setPointSize(10)
        self.lblType.setFont(font)
        self.lblType.setObjectName(_fromUtf8("lblType"))
        self.gridLayout.addWidget(self.lblType, 0, 2, 1, 1)
        self.cboType = QComboBox(self.fraParms)
        self.cboType.setObjectName(_fromUtf8("cboType"))
        self.gridLayout.addWidget(self.cboType, 0, 3, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.lblDescription = QLabel(self.fraParms)
        self.lblDescription.setObjectName(_fromUtf8("lblDescription"))
        self.gridLayout.addWidget(self.lblDescription, 1, 0, 1, 1)
        self.txtDescription = QLineEdit(self.fraParms)
        self.txtDescription.setObjectName(_fromUtf8("txtDescription"))
        self.gridLayout.addWidget(self.txtDescription, 1, 1, 1, 4)
        self.verticalLayout_2.addWidget(self.fraParms)
        self.fraBottom = QFrame(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraBottom.sizePolicy().hasHeightForWidth())
        self.fraBottom.setSizePolicy(sizePolicy)
        self.fraBottom.setFrameShape(QFrame.StyledPanel)
        self.fraBottom.setFrameShadow(QFrame.Raised)
        self.fraBottom.setObjectName(_fromUtf8("fraBottom"))
        self.horizontalLayout_2 = QHBoxLayout(self.fraBottom)
        # self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tblMult = QTableWidget(self.fraBottom)
        self.tblMult.setRowCount(24)
        self.tblMult.setColumnCount(1)
        self.tblMult.setObjectName(_fromUtf8("tblMult"))
        item = QTableWidgetItem()
        self.tblMult.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblMult.setHorizontalHeaderItem(0, item)
        self.horizontalLayout_2.addWidget(self.tblMult)
        self.fraRight = QFrame(self.fraBottom)
        self.fraRight.setFrameShape(QFrame.StyledPanel)
        self.fraRight.setFrameShadow(QFrame.Raised)
        self.fraRight.setObjectName(_fromUtf8("fraRight"))
        self.verticalLayout = QVBoxLayout(self.fraRight)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem1 = QSpacerItem(20, 128, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.fraOKCancel = QFrame(self.fraRight)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraOKCancel.sizePolicy().hasHeightForWidth())
        self.fraOKCancel.setSizePolicy(sizePolicy)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QSpacerItem(99, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        self.horizontalLayout_2.addWidget(self.fraRight)
        self.verticalLayout_2.addWidget(self.fraBottom)
        frmPatternEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmPatternEditor)
        QtCore.QMetaObject.connectSlotsByName(frmPatternEditor)

    def retranslateUi(self, frmPatternEditor):
        frmPatternEditor.setWindowTitle(_translate("frmPatternEditor", "SWMM Time Patterns", None))
        self.lblPatternID.setText(_translate("frmPatternEditor", "Pattern ID", None))
        self.lblType.setText(_translate("frmPatternEditor", "     Type", None))
        self.lblDescription.setText(_translate("frmPatternEditor", "<html><head/><body><p>Description</p></body></html>", None))
        item = self.tblMult.verticalHeaderItem(0)
        item.setText(_translate("frmPatternEditor", "1", None))
        item = self.tblMult.horizontalHeaderItem(0)
        item.setText(_translate("frmPatternEditor", "Multiplier", None))
        self.cmdOK.setText(_translate("frmPatternEditor", "OK", None))
        self.cmdCancel.setText(_translate("frmPatternEditor", "Cancel", None))

