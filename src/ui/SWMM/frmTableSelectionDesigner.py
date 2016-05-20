# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmTableSelectionDesigner.ui'
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

class Ui_frmTableSelection(object):
    def setupUi(self, frmTableSelection):
        frmTableSelection.setObjectName(_fromUtf8("frmTableSelection"))
        frmTableSelection.resize(416, 333)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTableSelection.setFont(font)
        self.centralWidget = QtGui.QWidget(frmTableSelection)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraTop = QtGui.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.gridLayout = QtGui.QGridLayout(self.fraTop)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cboObject = QtGui.QComboBox(self.fraTop)
        self.cboObject.setObjectName(_fromUtf8("cboObject"))
        self.gridLayout.addWidget(self.cboObject, 3, 1, 1, 1)
        self.lblTime = QtGui.QLabel(self.fraTop)
        self.lblTime.setObjectName(_fromUtf8("lblTime"))
        self.gridLayout.addWidget(self.lblTime, 2, 0, 1, 1)
        self.lblObject = QtGui.QLabel(self.fraTop)
        self.lblObject.setObjectName(_fromUtf8("lblObject"))
        self.gridLayout.addWidget(self.lblObject, 2, 1, 1, 1)
        self.cboTime = QtGui.QComboBox(self.fraTop)
        self.cboTime.setObjectName(_fromUtf8("cboTime"))
        self.gridLayout.addWidget(self.cboTime, 3, 0, 1, 1)
        self.lblVariables = QtGui.QLabel(self.fraTop)
        self.lblVariables.setObjectName(_fromUtf8("lblVariables"))
        self.gridLayout.addWidget(self.lblVariables, 4, 0, 1, 1)
        self.lblNodes = QtGui.QLabel(self.fraTop)
        self.lblNodes.setObjectName(_fromUtf8("lblNodes"))
        self.gridLayout.addWidget(self.lblNodes, 4, 1, 1, 1)
        self.cboEnd = QtGui.QComboBox(self.fraTop)
        self.cboEnd.setObjectName(_fromUtf8("cboEnd"))
        self.gridLayout.addWidget(self.cboEnd, 1, 1, 1, 1)
        self.lblEnd = QtGui.QLabel(self.fraTop)
        self.lblEnd.setObjectName(_fromUtf8("lblEnd"))
        self.gridLayout.addWidget(self.lblEnd, 0, 1, 1, 1)
        self.cboStart = QtGui.QComboBox(self.fraTop)
        self.cboStart.setObjectName(_fromUtf8("cboStart"))
        self.gridLayout.addWidget(self.cboStart, 1, 0, 1, 1)
        self.lblStart = QtGui.QLabel(self.fraTop)
        self.lblStart.setObjectName(_fromUtf8("lblStart"))
        self.gridLayout.addWidget(self.lblStart, 0, 0, 1, 1)
        self.lstNodes = QtGui.QListWidget(self.fraTop)
        self.lstNodes.setObjectName(_fromUtf8("lstNodes"))
        self.gridLayout.addWidget(self.lstNodes, 5, 1, 1, 1)
        self.lstVariables = QtGui.QListWidget(self.fraTop)
        self.lstVariables.setObjectName(_fromUtf8("lstVariables"))
        self.gridLayout.addWidget(self.lstVariables, 5, 0, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
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
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmTableSelection.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTableSelection)
        QtCore.QMetaObject.connectSlotsByName(frmTableSelection)

    def retranslateUi(self, frmTableSelection):
        frmTableSelection.setWindowTitle(_translate("frmTableSelection", "SWMM Table Selection", None))
        self.lblTime.setText(_translate("frmTableSelection", "Time Format", None))
        self.lblObject.setText(_translate("frmTableSelection", "Object Category", None))
        self.lblVariables.setText(_translate("frmTableSelection", "Variables", None))
        self.lblNodes.setText(_translate("frmTableSelection", "Nodes", None))
        self.lblEnd.setText(_translate("frmTableSelection", "End Date", None))
        self.lblStart.setText(_translate("frmTableSelection", "Start Date", None))
        self.cmdOK.setText(_translate("frmTableSelection", "OK", None))
        self.cmdCancel.setText(_translate("frmTableSelection", "Cancel", None))

