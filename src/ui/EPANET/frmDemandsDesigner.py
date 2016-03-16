# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmDemandsDesigner.ui'
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

class Ui_frmDemands(object):
    def setupUi(self, frmDemands):
        frmDemands.setObjectName(_fromUtf8("frmDemands"))
        frmDemands.resize(295, 265)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmDemands.setFont(font)
        self.centralWidget = QtGui.QWidget(frmDemands)
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
        self.tblDemands = QtGui.QTableWidget(self.fraTop)
        self.tblDemands.setRowCount(10)
        self.tblDemands.setObjectName(_fromUtf8("tblDemands"))
        self.tblDemands.setColumnCount(3)
        item = QtGui.QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tblDemands, 0, 0, 1, 1)
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

