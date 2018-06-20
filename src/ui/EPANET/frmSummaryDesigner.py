# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmSummaryDesigner.ui'
#
# Created: Wed Apr 19 11:09:15 2017
#      by: PyQt5 UI code generator 4.10.2
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

class Ui_frmSummary(object):
    def setupUi(self, frmSummary):
        frmSummary.setObjectName(_fromUtf8("frmSummary"))
        frmSummary.resize(541, 405)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmSummary.setFont(font)
        self.centralWidget = QWidget(frmSummary)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbxTitle = QGroupBox(self.centralWidget)
        self.gbxTitle.setObjectName(_fromUtf8("gbxTitle"))
        self.horizontalLayout_2 = QHBoxLayout(self.gbxTitle)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.txtTitle = QLineEdit(self.gbxTitle)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.horizontalLayout_2.addWidget(self.txtTitle)
        self.verticalLayout.addWidget(self.gbxTitle)
        self.gbxNotes = QGroupBox(self.centralWidget)
        self.gbxNotes.setObjectName(_fromUtf8("gbxNotes"))
        self.verticalLayout_2 = QVBoxLayout(self.gbxNotes)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.txtNotes = QPlainTextEdit(self.gbxNotes)
        self.txtNotes.setObjectName(_fromUtf8("txtNotes"))
        self.verticalLayout_2.addWidget(self.txtNotes)
        self.verticalLayout.addWidget(self.gbxNotes)
        self.gbxStats = QGroupBox(self.centralWidget)
        self.gbxStats.setObjectName(_fromUtf8("gbxStats"))
        self.verticalLayout_3 = QVBoxLayout(self.gbxStats)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.txtStats = QPlainTextEdit(self.gbxStats)
        self.txtStats.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.txtStats.setObjectName(_fromUtf8("txtStats"))
        self.verticalLayout_3.addWidget(self.txtStats)
        self.verticalLayout.addWidget(self.gbxStats)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
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
        frmSummary.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmSummary)
        QtCore.QMetaObject.connectSlotsByName(frmSummary)

    def retranslateUi(self, frmSummary):
        frmSummary.setWindowTitle(_translate("frmSummary", "EPANET Project Summary", None))
        self.gbxTitle.setTitle(_translate("frmSummary", "Title", None))
        self.gbxNotes.setTitle(_translate("frmSummary", "Notes", None))
        self.gbxStats.setTitle(_translate("frmSummary", "Statistics", None))
        self.cmdOK.setText(_translate("frmSummary", "OK", None))
        self.cmdCancel.setText(_translate("frmSummary", "Cancel", None))

