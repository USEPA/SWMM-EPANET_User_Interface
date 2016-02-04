# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmEnergyOptions.ui'
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

class Ui_frmEnergyOptions(object):
    def setupUi(self, frmEnergyOptions):
        frmEnergyOptions.setObjectName(_fromUtf8("frmEnergyOptions"))
        frmEnergyOptions.resize(304, 209)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmEnergyOptions.setFont(font)
        self.centralWidget = QtGui.QWidget(frmEnergyOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.lblGlobalEfficiency = QtGui.QLabel(self.centralWidget)
        self.lblGlobalEfficiency.setGeometry(QtCore.QRect(30, 20, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblGlobalEfficiency.setFont(font)
        self.lblGlobalEfficiency.setObjectName(_fromUtf8("lblGlobalEfficiency"))
        self.lblGlobalPrice = QtGui.QLabel(self.centralWidget)
        self.lblGlobalPrice.setGeometry(QtCore.QRect(30, 50, 101, 16))
        self.lblGlobalPrice.setObjectName(_fromUtf8("lblGlobalPrice"))
        self.lblGlobalPattern = QtGui.QLabel(self.centralWidget)
        self.lblGlobalPattern.setGeometry(QtCore.QRect(30, 80, 111, 16))
        self.lblGlobalPattern.setObjectName(_fromUtf8("lblGlobalPattern"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(60, 150, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(160, 150, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.txtGlobalPattern = QtGui.QLineEdit(self.centralWidget)
        self.txtGlobalPattern.setGeometry(QtCore.QRect(160, 80, 113, 20))
        self.txtGlobalPattern.setObjectName(_fromUtf8("txtGlobalPattern"))
        self.txtDemandCharge = QtGui.QLineEdit(self.centralWidget)
        self.txtDemandCharge.setGeometry(QtCore.QRect(160, 110, 113, 20))
        self.txtDemandCharge.setObjectName(_fromUtf8("txtDemandCharge"))
        self.lblDemandCharge = QtGui.QLabel(self.centralWidget)
        self.lblDemandCharge.setGeometry(QtCore.QRect(30, 110, 111, 16))
        self.lblDemandCharge.setObjectName(_fromUtf8("lblDemandCharge"))
        self.txtGlobalEfficiency = QtGui.QLineEdit(self.centralWidget)
        self.txtGlobalEfficiency.setGeometry(QtCore.QRect(160, 20, 113, 20))
        self.txtGlobalEfficiency.setObjectName(_fromUtf8("txtGlobalEfficiency"))
        self.txtGlobalPrice = QtGui.QLineEdit(self.centralWidget)
        self.txtGlobalPrice.setGeometry(QtCore.QRect(160, 50, 113, 20))
        self.txtGlobalPrice.setObjectName(_fromUtf8("txtGlobalPrice"))
        frmEnergyOptions.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtGui.QToolBar(frmEnergyOptions)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        frmEnergyOptions.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(frmEnergyOptions)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        frmEnergyOptions.setStatusBar(self.statusBar)

        self.retranslateUi(frmEnergyOptions)
        QtCore.QMetaObject.connectSlotsByName(frmEnergyOptions)

    def retranslateUi(self, frmEnergyOptions):
        frmEnergyOptions.setWindowTitle(_translate("frmEnergyOptions", "EPANET Energy Options", None))
        self.lblGlobalEfficiency.setText(_translate("frmEnergyOptions", "Pump Efficiency (%)", None))
        self.lblGlobalPrice.setText(_translate("frmEnergyOptions", "<html><head/><body><p>Energy Price/kwh</p></body></html>", None))
        self.lblGlobalPattern.setText(_translate("frmEnergyOptions", "Price Pattern", None))
        self.cmdOK.setText(_translate("frmEnergyOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmEnergyOptions", "Cancel", None))
        self.lblDemandCharge.setText(_translate("frmEnergyOptions", "Demand Charge", None))

