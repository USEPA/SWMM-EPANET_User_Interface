# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmInfiltrationDesigner.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frmInfiltrationEditor(object):
    def setupUi(self, frmInfiltrationEditor):
        frmInfiltrationEditor.setObjectName(_fromUtf8("frmInfiltrationEditor"))
        frmInfiltrationEditor.resize(391, 338)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmInfiltrationEditor.setFont(font)
        self.centralWidget = QtGui.QWidget(frmInfiltrationEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraTop = QtGui.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.fraTop)
        self.verticalLayout_3.setMargin(11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.lblTop = QtGui.QLabel(self.fraTop)
        self.lblTop.setObjectName(_fromUtf8("lblTop"))
        self.verticalLayout_3.addWidget(self.lblTop)
        self.tblGeneric = QtGui.QTableWidget(self.fraTop)
        self.tblGeneric.setObjectName(_fromUtf8("tblGeneric"))
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblGeneric.setHorizontalHeaderItem(0, item)
        self.verticalLayout_3.addWidget(self.tblGeneric)
        self.verticalLayout_2.addWidget(self.fraTop)
        self.fraNotes = QtGui.QFrame(self.centralWidget)
        self.fraNotes.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraNotes.setFrameShadow(QtGui.QFrame.Raised)
        self.fraNotes.setObjectName(_fromUtf8("fraNotes"))
        self.verticalLayout = QtGui.QVBoxLayout(self.fraNotes)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblNotes = QtGui.QLabel(self.fraNotes)
        self.lblNotes.setWordWrap(True)
        self.lblNotes.setObjectName(_fromUtf8("lblNotes"))
        self.verticalLayout.addWidget(self.lblNotes)
        self.verticalLayout_2.addWidget(self.fraNotes)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(338, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtGui.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmInfiltrationEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmInfiltrationEditor)
        QtCore.QMetaObject.connectSlotsByName(frmInfiltrationEditor)

    def retranslateUi(self, frmInfiltrationEditor):
        frmInfiltrationEditor.setWindowTitle(_translate("frmInfiltrationEditor", "SWMM Infiltration Editor", None))
        self.lblTop.setText(_translate("frmInfiltrationEditor", "<html><head/><body><p>Infiltration Method:  </p></body></html>", None))
        item = self.tblGeneric.horizontalHeaderItem(0)
        item.setText(_translate("frmInfiltrationEditor", "Value", None))
        self.lblNotes.setText(_translate("frmInfiltrationEditor", "Explanatory notes", None))
        self.cmdOK.setText(_translate("frmInfiltrationEditor", "OK", None))
        self.cmdCancel.setText(_translate("frmInfiltrationEditor", "Cancel", None))

