# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmInterfaceFilesDesigner.ui'
#
# Created: Tue Mar 08 16:50:37 2016
#      by: PyQt5 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
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

class Ui_frmInterfaceFiles(object):
    def setupUi(self, frmInterfaceFiles):
        frmInterfaceFiles.setObjectName(_fromUtf8("frmInterfaceFiles"))
        frmInterfaceFiles.resize(452, 342)
        font = QFont()
        font.setPointSize(10)
        frmInterfaceFiles.setFont(font)
        self.centralWidget = QWidget(frmInterfaceFiles)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.formLayout = QFormLayout(self.centralWidget)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblUseRainfall = QLabel(self.centralWidget)
        self.lblUseRainfall.setObjectName(_fromUtf8("lblUseRainfall"))
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblUseRainfall)
        self.txtUseRainfall = QLineEdit(self.centralWidget)
        self.txtUseRainfall.setObjectName(_fromUtf8("txtUseRainfall"))
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtUseRainfall)
        self.lblSaveRainfall = QLabel(self.centralWidget)
        self.lblSaveRainfall.setObjectName(_fromUtf8("lblSaveRainfall"))
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblSaveRainfall)
        self.txtSaveRainfall = QLineEdit(self.centralWidget)
        self.txtSaveRainfall.setObjectName(_fromUtf8("txtSaveRainfall"))
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.txtSaveRainfall)
        self.lblUseRunoff = QLabel(self.centralWidget)
        self.lblUseRunoff.setObjectName(_fromUtf8("lblUseRunoff"))
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblUseRunoff)
        self.txtUseRunoff = QLineEdit(self.centralWidget)
        self.txtUseRunoff.setObjectName(_fromUtf8("txtUseRunoff"))
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.txtUseRunoff)
        self.lblSaveRunoff = QLabel(self.centralWidget)
        self.lblSaveRunoff.setObjectName(_fromUtf8("lblSaveRunoff"))
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblSaveRunoff)
        self.txtSaveRunoff = QLineEdit(self.centralWidget)
        self.txtSaveRunoff.setObjectName(_fromUtf8("txtSaveRunoff"))
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.txtSaveRunoff)
        self.lblUseHotstart = QLabel(self.centralWidget)
        self.lblUseHotstart.setObjectName(_fromUtf8("lblUseHotstart"))
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblUseHotstart)
        self.txtUseHotstart = QLineEdit(self.centralWidget)
        self.txtUseHotstart.setObjectName(_fromUtf8("txtUseHotstart"))
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.txtUseHotstart)
        self.lblSaveHotstart = QLabel(self.centralWidget)
        self.lblSaveHotstart.setObjectName(_fromUtf8("lblSaveHotstart"))
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lblSaveHotstart)
        self.txtSaveHotstart = QLineEdit(self.centralWidget)
        self.txtSaveHotstart.setObjectName(_fromUtf8("txtSaveHotstart"))
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.txtSaveHotstart)
        self.lblUseRDII = QLabel(self.centralWidget)
        self.lblUseRDII.setObjectName(_fromUtf8("lblUseRDII"))
        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.lblUseRDII)
        self.txtUseRDII = QLineEdit(self.centralWidget)
        self.txtUseRDII.setObjectName(_fromUtf8("txtUseRDII"))
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.txtUseRDII)
        self.lblSaveRDII = QLabel(self.centralWidget)
        self.lblSaveRDII.setObjectName(_fromUtf8("lblSaveRDII"))
        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.lblSaveRDII)
        self.txtSaveRDII = QLineEdit(self.centralWidget)
        self.txtSaveRDII.setObjectName(_fromUtf8("txtSaveRDII"))
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.txtSaveRDII)
        self.lblUseInflows = QLabel(self.centralWidget)
        self.lblUseInflows.setObjectName(_fromUtf8("lblUseInflows"))
        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.lblUseInflows)
        self.txtUseInflows = QLineEdit(self.centralWidget)
        self.txtUseInflows.setObjectName(_fromUtf8("txtUseInflows"))
        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.txtUseInflows)
        self.lblSaveOutflows = QLabel(self.centralWidget)
        self.lblSaveOutflows.setObjectName(_fromUtf8("lblSaveOutflows"))
        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.lblSaveOutflows)
        self.txtSaveOutflows = QLineEdit(self.centralWidget)
        self.txtSaveOutflows.setObjectName(_fromUtf8("txtSaveOutflows"))
        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.txtSaveOutflows)
        self.frame = QFrame(self.centralWidget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(249, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.frame)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.frame)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.formLayout.setWidget(10, QFormLayout.SpanningRole, self.frame)
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

