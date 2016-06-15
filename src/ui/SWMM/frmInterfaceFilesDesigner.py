# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmInterfaceFilesDesigner.ui'
#
# Created: Tue Mar 08 16:50:37 2016
#      by: PyQt4 UI code generator 4.11.3
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
        frmInterfaceFiles.resize(452, 342)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmInterfaceFiles.setFont(font)
        self.centralWidget = QtGui.QWidget(frmInterfaceFiles)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.formLayout = QtGui.QFormLayout(self.centralWidget)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblUseRainfall = QtGui.QLabel(self.centralWidget)
        self.lblUseRainfall.setObjectName(_fromUtf8("lblUseRainfall"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblUseRainfall)
        self.txtUseRainfall = QtGui.QLineEdit(self.centralWidget)
        self.txtUseRainfall.setObjectName(_fromUtf8("txtUseRainfall"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtUseRainfall)
        self.lblSaveRainfall = QtGui.QLabel(self.centralWidget)
        self.lblSaveRainfall.setObjectName(_fromUtf8("lblSaveRainfall"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblSaveRainfall)
        self.txtSaveRainfall = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveRainfall.setObjectName(_fromUtf8("txtSaveRainfall"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtSaveRainfall)
        self.lblUseRunoff = QtGui.QLabel(self.centralWidget)
        self.lblUseRunoff.setObjectName(_fromUtf8("lblUseRunoff"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblUseRunoff)
        self.txtUseRunoff = QtGui.QLineEdit(self.centralWidget)
        self.txtUseRunoff.setObjectName(_fromUtf8("txtUseRunoff"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.txtUseRunoff)
        self.lblSaveRunoff = QtGui.QLabel(self.centralWidget)
        self.lblSaveRunoff.setObjectName(_fromUtf8("lblSaveRunoff"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lblSaveRunoff)
        self.txtSaveRunoff = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveRunoff.setObjectName(_fromUtf8("txtSaveRunoff"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.txtSaveRunoff)
        self.lblUseHotstart = QtGui.QLabel(self.centralWidget)
        self.lblUseHotstart.setObjectName(_fromUtf8("lblUseHotstart"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.lblUseHotstart)
        self.txtUseHotstart = QtGui.QLineEdit(self.centralWidget)
        self.txtUseHotstart.setObjectName(_fromUtf8("txtUseHotstart"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.txtUseHotstart)
        self.lblSaveHotstart = QtGui.QLabel(self.centralWidget)
        self.lblSaveHotstart.setObjectName(_fromUtf8("lblSaveHotstart"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.lblSaveHotstart)
        self.txtSaveHotstart = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveHotstart.setObjectName(_fromUtf8("txtSaveHotstart"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.txtSaveHotstart)
        self.lblUseRDII = QtGui.QLabel(self.centralWidget)
        self.lblUseRDII.setObjectName(_fromUtf8("lblUseRDII"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.lblUseRDII)
        self.txtUseRDII = QtGui.QLineEdit(self.centralWidget)
        self.txtUseRDII.setObjectName(_fromUtf8("txtUseRDII"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.txtUseRDII)
        self.lblSaveRDII = QtGui.QLabel(self.centralWidget)
        self.lblSaveRDII.setObjectName(_fromUtf8("lblSaveRDII"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.lblSaveRDII)
        self.txtSaveRDII = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveRDII.setObjectName(_fromUtf8("txtSaveRDII"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.txtSaveRDII)
        self.lblUseInflows = QtGui.QLabel(self.centralWidget)
        self.lblUseInflows.setObjectName(_fromUtf8("lblUseInflows"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.lblUseInflows)
        self.txtUseInflows = QtGui.QLineEdit(self.centralWidget)
        self.txtUseInflows.setObjectName(_fromUtf8("txtUseInflows"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.txtUseInflows)
        self.lblSaveOutflows = QtGui.QLabel(self.centralWidget)
        self.lblSaveOutflows.setObjectName(_fromUtf8("lblSaveOutflows"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.lblSaveOutflows)
        self.txtSaveOutflows = QtGui.QLineEdit(self.centralWidget)
        self.txtSaveOutflows.setObjectName(_fromUtf8("txtSaveOutflows"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.txtSaveOutflows)
        self.frame = QtGui.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(249, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtGui.QPushButton(self.frame)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.frame)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.formLayout.setWidget(10, QtGui.QFormLayout.SpanningRole, self.frame)
        frmInterfaceFiles.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmInterfaceFiles)
        QtCore.QMetaObject.connectSlotsByName(frmInterfaceFiles)
        frmInterfaceFiles.setTabOrder(self.txtUseRainfall, self.txtSaveRainfall)
        frmInterfaceFiles.setTabOrder(self.txtSaveRainfall, self.txtUseRunoff)
        frmInterfaceFiles.setTabOrder(self.txtUseRunoff, self.txtSaveRunoff)
        frmInterfaceFiles.setTabOrder(self.txtSaveRunoff, self.txtUseHotstart)
        frmInterfaceFiles.setTabOrder(self.txtUseHotstart, self.txtSaveHotstart)
        frmInterfaceFiles.setTabOrder(self.txtSaveHotstart, self.txtUseRDII)
        frmInterfaceFiles.setTabOrder(self.txtUseRDII, self.txtSaveRDII)
        frmInterfaceFiles.setTabOrder(self.txtSaveRDII, self.txtUseInflows)
        frmInterfaceFiles.setTabOrder(self.txtUseInflows, self.txtSaveOutflows)
        frmInterfaceFiles.setTabOrder(self.txtSaveOutflows, self.cmdOK)
        frmInterfaceFiles.setTabOrder(self.cmdOK, self.cmdCancel)

    def retranslateUi(self, frmInterfaceFiles):
        frmInterfaceFiles.setWindowTitle(_translate("frmInterfaceFiles", "SWMM Interface File Options", None))
        self.lblUseRainfall.setText(_translate("frmInterfaceFiles", "<html><head/><body><p>Use Rainfall</p></body></html>", None))
        self.lblSaveRainfall.setText(_translate("frmInterfaceFiles", "Save Rainfall", None))
        self.lblUseRunoff.setText(_translate("frmInterfaceFiles", "Use Runoff", None))
        self.lblSaveRunoff.setText(_translate("frmInterfaceFiles", "Save Runoff", None))
        self.lblUseHotstart.setText(_translate("frmInterfaceFiles", "Use Hotstart", None))
        self.lblSaveHotstart.setText(_translate("frmInterfaceFiles", "Save Hotstart", None))
        self.lblUseRDII.setText(_translate("frmInterfaceFiles", "Use RDII", None))
        self.lblSaveRDII.setText(_translate("frmInterfaceFiles", "Save RDII", None))
        self.lblUseInflows.setText(_translate("frmInterfaceFiles", "Use Inflows", None))
        self.lblSaveOutflows.setText(_translate("frmInterfaceFiles", "Save Outflows", None))
        self.cmdOK.setText(_translate("frmInterfaceFiles", "OK", None))
        self.cmdCancel.setText(_translate("frmInterfaceFiles", "Cancel", None))

