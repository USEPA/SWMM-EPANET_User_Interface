# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmInterfaceFiles.ui'
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

class Ui_frmInterfaceFiles(object):
    def setupUi(self, frmInterfaceFiles):
        frmInterfaceFiles.setObjectName(_fromUtf8("frmInterfaceFiles"))
        frmInterfaceFiles.resize(395, 458)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmInterfaceFiles.setFont(font)
        self.centralWidget = QtGui.QWidget(frmInterfaceFiles)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(110, 420, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(210, 420, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.lblUseRainfall = QtGui.QLabel(self.centralWidget)
        self.lblUseRainfall.setGeometry(QtCore.QRect(30, 20, 141, 16))
        self.lblUseRainfall.setObjectName(_fromUtf8("lblUseRainfall"))
        self.lblSaveRainfall = QtGui.QLabel(self.centralWidget)
        self.lblSaveRainfall.setGeometry(QtCore.QRect(30, 60, 141, 16))
        self.lblSaveRainfall.setObjectName(_fromUtf8("lblSaveRainfall"))
        self.lblUseRunoff = QtGui.QLabel(self.centralWidget)
        self.lblUseRunoff.setGeometry(QtCore.QRect(30, 100, 141, 16))
        self.lblUseRunoff.setObjectName(_fromUtf8("lblUseRunoff"))
        self.lblUseHotstart = QtGui.QLabel(self.centralWidget)
        self.lblUseHotstart.setGeometry(QtCore.QRect(30, 180, 211, 16))
        self.lblUseHotstart.setObjectName(_fromUtf8("lblUseHotstart"))
        self.lblSaveHotstart = QtGui.QLabel(self.centralWidget)
        self.lblSaveHotstart.setGeometry(QtCore.QRect(30, 220, 251, 16))
        self.lblSaveHotstart.setObjectName(_fromUtf8("lblSaveHotstart"))
        self.lblUseRDII = QtGui.QLabel(self.centralWidget)
        self.lblUseRDII.setGeometry(QtCore.QRect(30, 260, 251, 16))
        self.lblUseRDII.setObjectName(_fromUtf8("lblUseRDII"))
        self.lblSaveRDII = QtGui.QLabel(self.centralWidget)
        self.lblSaveRDII.setGeometry(QtCore.QRect(30, 300, 251, 16))
        self.lblSaveRDII.setObjectName(_fromUtf8("lblSaveRDII"))
        self.lblUseInflows = QtGui.QLabel(self.centralWidget)
        self.lblUseInflows.setGeometry(QtCore.QRect(30, 340, 251, 16))
        self.lblUseInflows.setObjectName(_fromUtf8("lblUseInflows"))
        self.lblSaveOutflows = QtGui.QLabel(self.centralWidget)
        self.lblSaveOutflows.setGeometry(QtCore.QRect(30, 380, 251, 16))
        self.lblSaveOutflows.setObjectName(_fromUtf8("lblSaveOutflows"))
        self.txtUseInflows = QtGui.QLineEdit(self.centralWidget)
        self.txtUseInflows.setGeometry(QtCore.QRect(130, 340, 231, 20))
        self.txtUseInflows.setObjectName(_fromUtf8("txtUseInflows"))
        self.lblSaveRunoff = QtGui.QLabel(self.centralWidget)
        self.lblSaveRunoff.setGeometry(QtCore.QRect(30, 140, 141, 16))
        self.lblSaveRunoff.setObjectName(_fromUtf8("lblSaveRunoff"))
        self.txtSaveOutflows = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveOutflows.setGeometry(QtCore.QRect(130, 380, 231, 20))
        self.txtSaveOutflows.setObjectName(_fromUtf8("txtSaveOutflows"))
        self.txtSaveRDII = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveRDII.setGeometry(QtCore.QRect(130, 300, 231, 20))
        self.txtSaveRDII.setObjectName(_fromUtf8("txtSaveRDII"))
        self.txtUseRDII = QtGui.QLineEdit(self.centralWidget)
        self.txtUseRDII.setGeometry(QtCore.QRect(130, 260, 231, 20))
        self.txtUseRDII.setObjectName(_fromUtf8("txtUseRDII"))
        self.txtSaveHotstart = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveHotstart.setGeometry(QtCore.QRect(130, 220, 231, 20))
        self.txtSaveHotstart.setObjectName(_fromUtf8("txtSaveHotstart"))
        self.txtUseHotstart = QtGui.QLineEdit(self.centralWidget)
        self.txtUseHotstart.setGeometry(QtCore.QRect(130, 180, 231, 20))
        self.txtUseHotstart.setObjectName(_fromUtf8("txtUseHotstart"))
        self.txtSaveRunoff = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveRunoff.setGeometry(QtCore.QRect(130, 140, 231, 20))
        self.txtSaveRunoff.setObjectName(_fromUtf8("txtSaveRunoff"))
        self.txtUseRunoff = QtGui.QLineEdit(self.centralWidget)
        self.txtUseRunoff.setGeometry(QtCore.QRect(130, 100, 231, 20))
        self.txtUseRunoff.setObjectName(_fromUtf8("txtUseRunoff"))
        self.txtSaveRainfall = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveRainfall.setGeometry(QtCore.QRect(130, 60, 231, 20))
        self.txtSaveRainfall.setObjectName(_fromUtf8("txtSaveRainfall"))
        self.txtUseRainfall = QtGui.QLineEdit(self.centralWidget)
        self.txtUseRainfall.setGeometry(QtCore.QRect(130, 20, 231, 20))
        self.txtUseRainfall.setObjectName(_fromUtf8("txtUseRainfall"))
        frmInterfaceFiles.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmInterfaceFiles)
        QtCore.QMetaObject.connectSlotsByName(frmInterfaceFiles)

    def retranslateUi(self, frmInterfaceFiles):
        frmInterfaceFiles.setWindowTitle(_translate("frmInterfaceFiles", "SWMM Interface File Options", None))
        self.cmdOK.setText(_translate("frmInterfaceFiles", "OK", None))
        self.cmdCancel.setText(_translate("frmInterfaceFiles", "Cancel", None))
        self.lblUseRainfall.setText(_translate("frmInterfaceFiles", "<html><head/><body><p>Use Rainfall</p></body></html>", None))
        self.lblSaveRainfall.setText(_translate("frmInterfaceFiles", "Save Rainfall", None))
        self.lblUseRunoff.setText(_translate("frmInterfaceFiles", "Use Runoff", None))
        self.lblUseHotstart.setText(_translate("frmInterfaceFiles", "Use Hotstart", None))
        self.lblSaveHotstart.setText(_translate("frmInterfaceFiles", "Save Hotstart", None))
        self.lblUseRDII.setText(_translate("frmInterfaceFiles", "Use RDII", None))
        self.lblSaveRDII.setText(_translate("frmInterfaceFiles", "Save RDII", None))
        self.lblUseInflows.setText(_translate("frmInterfaceFiles", "Use Inflows", None))
        self.lblSaveOutflows.setText(_translate("frmInterfaceFiles", "Save Outflows", None))
        self.lblSaveRunoff.setText(_translate("frmInterfaceFiles", "Save Runoff", None))

