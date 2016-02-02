# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\SWMM-EPANET_User_Interface\src\ui\plugins\EPANET\frmMapBackdropOptions.ui'
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
        frmHydraulicsOptions.resize(562, 410)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmHydraulicsOptions.setFont(font)
        self.centralWidget = QtGui.QWidget(frmHydraulicsOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.lblMapFile = QtGui.QLabel(self.centralWidget)
        self.lblMapFile.setGeometry(QtCore.QRect(30, 20, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblMapFile.setFont(font)
        self.lblMapFile.setObjectName(_fromUtf8("lblMapFile"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(190, 350, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(290, 350, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.cboMapUnits = QtGui.QComboBox(self.centralWidget)
        self.cboMapUnits.setGeometry(QtCore.QRect(160, 200, 111, 22))
        self.cboMapUnits.setObjectName(_fromUtf8("cboMapUnits"))
        self.txtMapFile = QtGui.QLineEdit(self.centralWidget)
        self.txtMapFile.setGeometry(QtCore.QRect(160, 20, 341, 20))
        self.txtMapFile.setObjectName(_fromUtf8("txtMapFile"))
        self.gbxMap = QtGui.QGroupBox(self.centralWidget)
        self.gbxMap.setGeometry(QtCore.QRect(30, 50, 511, 141))
        self.gbxMap.setObjectName(_fromUtf8("gbxMap"))
        self.gbxLL = QtGui.QGroupBox(self.gbxMap)
        self.gbxLL.setGeometry(QtCore.QRect(20, 30, 231, 91))
        self.gbxLL.setObjectName(_fromUtf8("gbxLL"))
        self.lblLLX = QtGui.QLabel(self.gbxLL)
        self.lblLLX.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.lblLLX.setObjectName(_fromUtf8("lblLLX"))
        self.lblLLY = QtGui.QLabel(self.gbxLL)
        self.lblLLY.setGeometry(QtCore.QRect(20, 50, 111, 16))
        self.lblLLY.setObjectName(_fromUtf8("lblLLY"))
        self.txtLLX = QtGui.QLineEdit(self.gbxLL)
        self.txtLLX.setGeometry(QtCore.QRect(100, 30, 113, 20))
        self.txtLLX.setObjectName(_fromUtf8("txtLLX"))
        self.txtLLY = QtGui.QLineEdit(self.gbxLL)
        self.txtLLY.setGeometry(QtCore.QRect(100, 50, 113, 20))
        self.txtLLY.setObjectName(_fromUtf8("txtLLY"))
        self.gbxUR = QtGui.QGroupBox(self.gbxMap)
        self.gbxUR.setGeometry(QtCore.QRect(260, 30, 231, 91))
        self.gbxUR.setObjectName(_fromUtf8("gbxUR"))
        self.lblURX = QtGui.QLabel(self.gbxUR)
        self.lblURX.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.lblURX.setObjectName(_fromUtf8("lblURX"))
        self.txtURY = QtGui.QLineEdit(self.gbxUR)
        self.txtURY.setGeometry(QtCore.QRect(100, 50, 113, 20))
        self.txtURY.setObjectName(_fromUtf8("txtURY"))
        self.txtURX = QtGui.QLineEdit(self.gbxUR)
        self.txtURX.setGeometry(QtCore.QRect(100, 30, 113, 20))
        self.txtURX.setObjectName(_fromUtf8("txtURX"))
        self.lblURY = QtGui.QLabel(self.gbxUR)
        self.lblURY.setGeometry(QtCore.QRect(20, 50, 111, 16))
        self.lblURY.setObjectName(_fromUtf8("lblURY"))
        self.lblMapUnits = QtGui.QLabel(self.centralWidget)
        self.lblMapUnits.setGeometry(QtCore.QRect(30, 200, 111, 16))
        self.lblMapUnits.setObjectName(_fromUtf8("lblMapUnits"))
        self.lblBackdrop = QtGui.QLabel(self.centralWidget)
        self.lblBackdrop.setGeometry(QtCore.QRect(30, 230, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblBackdrop.setFont(font)
        self.lblBackdrop.setObjectName(_fromUtf8("lblBackdrop"))
        self.txtBackdropFile = QtGui.QLineEdit(self.centralWidget)
        self.txtBackdropFile.setGeometry(QtCore.QRect(160, 230, 341, 20))
        self.txtBackdropFile.setObjectName(_fromUtf8("txtBackdropFile"))
        self.gbxBackdrop = QtGui.QGroupBox(self.centralWidget)
        self.gbxBackdrop.setGeometry(QtCore.QRect(20, 260, 521, 71))
        self.gbxBackdrop.setObjectName(_fromUtf8("gbxBackdrop"))
        self.lblX = QtGui.QLabel(self.gbxBackdrop)
        self.lblX.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.lblX.setObjectName(_fromUtf8("lblX"))
        self.lblY = QtGui.QLabel(self.gbxBackdrop)
        self.lblY.setGeometry(QtCore.QRect(170, 30, 111, 16))
        self.lblY.setObjectName(_fromUtf8("lblY"))
        self.txtBackdropX = QtGui.QLineEdit(self.gbxBackdrop)
        self.txtBackdropX.setGeometry(QtCore.QRect(40, 30, 113, 20))
        self.txtBackdropX.setObjectName(_fromUtf8("txtBackdropX"))
        self.txtBackdropY = QtGui.QLineEdit(self.gbxBackdrop)
        self.txtBackdropY.setGeometry(QtCore.QRect(190, 30, 113, 20))
        self.txtBackdropY.setObjectName(_fromUtf8("txtBackdropY"))
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
        self.lblMapFile.setText(_translate("frmHydraulicsOptions", "Map File Name", None))
        self.cmdOK.setText(_translate("frmHydraulicsOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmHydraulicsOptions", "Cancel", None))
        self.gbxMap.setTitle(_translate("frmHydraulicsOptions", "Map Dimensions", None))
        self.gbxLL.setTitle(_translate("frmHydraulicsOptions", "Lower Left", None))
        self.lblLLX.setText(_translate("frmHydraulicsOptions", "X-Coordinate", None))
        self.lblLLY.setText(_translate("frmHydraulicsOptions", "Y-Coordinate", None))
        self.gbxUR.setTitle(_translate("frmHydraulicsOptions", "Upper Right", None))
        self.lblURX.setText(_translate("frmHydraulicsOptions", "X-Coordinate", None))
        self.lblURY.setText(_translate("frmHydraulicsOptions", "Y-Coordinate", None))
        self.lblMapUnits.setText(_translate("frmHydraulicsOptions", "Map Units", None))
        self.lblBackdrop.setText(_translate("frmHydraulicsOptions", "Backdrop File Name", None))
        self.gbxBackdrop.setTitle(_translate("frmHydraulicsOptions", "Backdrop Offsets", None))
        self.lblX.setText(_translate("frmHydraulicsOptions", "X", None))
        self.lblY.setText(_translate("frmHydraulicsOptions", "Y", None))

