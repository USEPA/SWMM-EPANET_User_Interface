# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmEnergyOptionsDesigner.ui'
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
        frmEnergyOptions.resize(302, 194)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmEnergyOptions.setFont(font)
        self.centralWidget = QtGui.QWidget(frmEnergyOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraParms = QtGui.QFrame(self.centralWidget)
        self.fraParms.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraParms.setFrameShadow(QtGui.QFrame.Raised)
        self.fraParms.setObjectName(_fromUtf8("fraParms"))
        self.gridLayout = QtGui.QGridLayout(self.fraParms)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblGlobalEfficiency = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblGlobalEfficiency.setFont(font)
        self.lblGlobalEfficiency.setObjectName(_fromUtf8("lblGlobalEfficiency"))
        self.gridLayout.addWidget(self.lblGlobalEfficiency, 0, 0, 1, 1)
        self.txtGlobalEfficiency = QtGui.QLineEdit(self.fraParms)
        self.txtGlobalEfficiency.setObjectName(_fromUtf8("txtGlobalEfficiency"))
        self.gridLayout.addWidget(self.txtGlobalEfficiency, 0, 1, 1, 1)
        self.lblGlobalPrice = QtGui.QLabel(self.fraParms)
        self.lblGlobalPrice.setObjectName(_fromUtf8("lblGlobalPrice"))
        self.gridLayout.addWidget(self.lblGlobalPrice, 1, 0, 1, 1)
        self.txtGlobalPrice = QtGui.QLineEdit(self.fraParms)
        self.txtGlobalPrice.setObjectName(_fromUtf8("txtGlobalPrice"))
        self.gridLayout.addWidget(self.txtGlobalPrice, 1, 1, 1, 1)
        self.lblGlobalPattern = QtGui.QLabel(self.fraParms)
        self.lblGlobalPattern.setObjectName(_fromUtf8("lblGlobalPattern"))
        self.gridLayout.addWidget(self.lblGlobalPattern, 2, 0, 1, 1)
        self.txtGlobalPattern = QtGui.QLineEdit(self.fraParms)
        self.txtGlobalPattern.setObjectName(_fromUtf8("txtGlobalPattern"))
        self.gridLayout.addWidget(self.txtGlobalPattern, 2, 1, 1, 1)
        self.lblDemandCharge = QtGui.QLabel(self.fraParms)
        self.lblDemandCharge.setObjectName(_fromUtf8("lblDemandCharge"))
        self.gridLayout.addWidget(self.lblDemandCharge, 3, 0, 1, 1)
        self.txtDemandCharge = QtGui.QLineEdit(self.fraParms)
        self.txtDemandCharge.setObjectName(_fromUtf8("txtDemandCharge"))
        self.gridLayout.addWidget(self.txtDemandCharge, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.fraParms)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(99, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtGui.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmEnergyOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmEnergyOptions)
        QtCore.QMetaObject.connectSlotsByName(frmEnergyOptions)

    def retranslateUi(self, frmEnergyOptions):
        frmEnergyOptions.setWindowTitle(_translate("frmEnergyOptions", "EPANET Energy Options", None))
        self.lblGlobalEfficiency.setText(_translate("frmEnergyOptions", "Pump Efficiency (%)", None))
        self.lblGlobalPrice.setText(_translate("frmEnergyOptions", "<html><head/><body><p>Energy Price/kwh</p></body></html>", None))
        self.lblGlobalPattern.setText(_translate("frmEnergyOptions", "Price Pattern", None))
        self.lblDemandCharge.setText(_translate("frmEnergyOptions", "Demand Charge", None))
        self.cmdOK.setText(_translate("frmEnergyOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmEnergyOptions", "Cancel", None))

