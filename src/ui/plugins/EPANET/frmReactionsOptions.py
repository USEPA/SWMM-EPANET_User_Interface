# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\SWMM-EPANET_User_Interface\src\ui\plugins\EPANET\frmReactionsOptions.ui'
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

class Ui_frmHydraulicsOptions(object):
    def setupUi(self, frmHydraulicsOptions):
        frmHydraulicsOptions.setObjectName(_fromUtf8("frmHydraulicsOptions"))
        frmHydraulicsOptions.resize(345, 295)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmHydraulicsOptions.setFont(font)
        self.centralWidget = QtGui.QWidget(frmHydraulicsOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.lblBulkOrder = QtGui.QLabel(self.centralWidget)
        self.lblBulkOrder.setGeometry(QtCore.QRect(30, 20, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblBulkOrder.setFont(font)
        self.lblBulkOrder.setObjectName(_fromUtf8("lblBulkOrder"))
        self.lblWallOrder = QtGui.QLabel(self.centralWidget)
        self.lblWallOrder.setGeometry(QtCore.QRect(30, 50, 121, 16))
        self.lblWallOrder.setObjectName(_fromUtf8("lblWallOrder"))
        self.lblTankOrder = QtGui.QLabel(self.centralWidget)
        self.lblTankOrder.setGeometry(QtCore.QRect(30, 80, 121, 16))
        self.lblTankOrder.setObjectName(_fromUtf8("lblTankOrder"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(80, 240, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(180, 240, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.txtTankOrder = QtGui.QLineEdit(self.centralWidget)
        self.txtTankOrder.setGeometry(QtCore.QRect(200, 80, 113, 20))
        self.txtTankOrder.setObjectName(_fromUtf8("txtTankOrder"))
        self.lblGlobalBulk = QtGui.QLabel(self.centralWidget)
        self.lblGlobalBulk.setGeometry(QtCore.QRect(30, 110, 131, 16))
        self.lblGlobalBulk.setObjectName(_fromUtf8("lblGlobalBulk"))
        self.txtGlobalBulk = QtGui.QLineEdit(self.centralWidget)
        self.txtGlobalBulk.setGeometry(QtCore.QRect(200, 110, 113, 20))
        self.txtGlobalBulk.setObjectName(_fromUtf8("txtGlobalBulk"))
        self.lblGlobalWall = QtGui.QLabel(self.centralWidget)
        self.lblGlobalWall.setGeometry(QtCore.QRect(30, 140, 131, 16))
        self.lblGlobalWall.setObjectName(_fromUtf8("lblGlobalWall"))
        self.txtGlobalWall = QtGui.QLineEdit(self.centralWidget)
        self.txtGlobalWall.setGeometry(QtCore.QRect(200, 140, 113, 20))
        self.txtGlobalWall.setObjectName(_fromUtf8("txtGlobalWall"))
        self.lblLimiting = QtGui.QLabel(self.centralWidget)
        self.lblLimiting.setGeometry(QtCore.QRect(30, 170, 131, 16))
        self.lblLimiting.setObjectName(_fromUtf8("lblLimiting"))
        self.lblCorrelation = QtGui.QLabel(self.centralWidget)
        self.lblCorrelation.setGeometry(QtCore.QRect(30, 200, 171, 16))
        self.lblCorrelation.setObjectName(_fromUtf8("lblCorrelation"))
        self.txtLimiting = QtGui.QLineEdit(self.centralWidget)
        self.txtLimiting.setGeometry(QtCore.QRect(200, 170, 113, 20))
        self.txtLimiting.setObjectName(_fromUtf8("txtLimiting"))
        self.txtCorrelation = QtGui.QLineEdit(self.centralWidget)
        self.txtCorrelation.setGeometry(QtCore.QRect(200, 200, 113, 20))
        self.txtCorrelation.setObjectName(_fromUtf8("txtCorrelation"))
        self.txtBulkOrder = QtGui.QLineEdit(self.centralWidget)
        self.txtBulkOrder.setGeometry(QtCore.QRect(200, 20, 113, 20))
        self.txtBulkOrder.setObjectName(_fromUtf8("txtBulkOrder"))
        self.txtWallOrder = QtGui.QLineEdit(self.centralWidget)
        self.txtWallOrder.setGeometry(QtCore.QRect(200, 50, 113, 20))
        self.txtWallOrder.setObjectName(_fromUtf8("txtWallOrder"))
        frmHydraulicsOptions.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtGui.QToolBar(frmHydraulicsOptions)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        frmHydraulicsOptions.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(frmHydraulicsOptions)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        frmHydraulicsOptions.setStatusBar(self.statusBar)

        self.retranslateUi(frmHydraulicsOptions)
        QtCore.QMetaObject.connectSlotsByName(frmHydraulicsOptions)

    def retranslateUi(self, frmHydraulicsOptions):
        frmHydraulicsOptions.setWindowTitle(_translate("frmHydraulicsOptions", "EPANET Hydraulics Options", None))
        self.lblBulkOrder.setText(_translate("frmHydraulicsOptions", "Bulk Reaction Order", None))
        self.lblWallOrder.setText(_translate("frmHydraulicsOptions", "<html><head/><body><p>Wall Reaction Order</p></body></html>", None))
        self.lblTankOrder.setText(_translate("frmHydraulicsOptions", "Tank Reaction Order", None))
        self.cmdOK.setText(_translate("frmHydraulicsOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmHydraulicsOptions", "Cancel", None))
        self.lblGlobalBulk.setText(_translate("frmHydraulicsOptions", "Global Bulk Coefficient", None))
        self.lblGlobalWall.setText(_translate("frmHydraulicsOptions", "Global Wall Coefficient", None))
        self.lblLimiting.setText(_translate("frmHydraulicsOptions", "Limiting Concentration", None))
        self.lblCorrelation.setText(_translate("frmHydraulicsOptions", "Wall Roughness Correlation", None))

