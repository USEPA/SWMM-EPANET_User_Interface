# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmMapAddVectorDesigner.ui'
#
# Created: Sat Jan 16 15:12:00 2016
#      by: PyQt5 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
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

class Ui_frmAddVectorLayer(object):
    def setupUi(self, frmAddVectorLayer):
        frmAddVectorLayer.setObjectName(_fromUtf8("frmAddVectorLayer"))
        frmAddVectorLayer.resize(453, 215)
        self.verticalLayout = QVBoxLayout(frmAddVectorLayer)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QGroupBox(frmAddVectorLayer)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rdoDirectory = QRadioButton(self.groupBox)
        self.rdoDirectory.setObjectName(_fromUtf8("rdoDirectory"))
        self.gridLayout.addWidget(self.rdoDirectory, 0, 1, 1, 1)
        self.rdoDatabase = QRadioButton(self.groupBox)
        self.rdoDatabase.setObjectName(_fromUtf8("rdoDatabase"))
        self.gridLayout.addWidget(self.rdoDatabase, 0, 2, 1, 1)
        self.lblEncoding = QLabel(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEncoding.sizePolicy().hasHeightForWidth())
        self.lblEncoding.setSizePolicy(sizePolicy)
        self.lblEncoding.setObjectName(_fromUtf8("lblEncoding"))
        self.gridLayout.addWidget(self.lblEncoding, 2, 0, 1, 1)
        self.rdoFile = QRadioButton(self.groupBox)
        self.rdoFile.setObjectName(_fromUtf8("rdoFile"))
        self.gridLayout.addWidget(self.rdoFile, 0, 0, 1, 1)
        self.rdoProtocol = QRadioButton(self.groupBox)
        self.rdoProtocol.setObjectName(_fromUtf8("rdoProtocol"))
        self.gridLayout.addWidget(self.rdoProtocol, 0, 3, 1, 1)
        self.cboEncoding = QComboBox(self.groupBox)
        self.cboEncoding.setObjectName(_fromUtf8("cboEncoding"))
        self.gridLayout.addWidget(self.cboEncoding, 2, 1, 1, 3)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(frmAddVectorLayer)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblDataset = QLabel(self.groupBox_2)
        self.lblDataset.setObjectName(_fromUtf8("lblDataset"))
        self.horizontalLayout.addWidget(self.lblDataset)
        self.txtDataset = QLineEdit(self.groupBox_2)
        self.txtDataset.setObjectName(_fromUtf8("txtDataset"))
        self.horizontalLayout.addWidget(self.txtDataset)
        self.btnBrowse = QPushButton(self.groupBox_2)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.btnBox = QDialogButtonBox(frmAddVectorLayer)
        self.btnBox.setOrientation(QtCore.Qt.Horizontal)
        self.btnBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Open)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.verticalLayout.addWidget(self.btnBox)
        self.actionBtnBox_Clicked = QAction(frmAddVectorLayer)
        self.actionBtnBox_Clicked.setObjectName(_fromUtf8("actionBtnBox_Clicked"))
        self.actionBrowse_Clicked = QAction(frmAddVectorLayer)
        self.actionBrowse_Clicked.setObjectName(_fromUtf8("actionBrowse_Clicked"))

        self.retranslateUi(frmAddVectorLayer)
        self.btnBox.accepted.connect(frmAddVectorLayer.accept)
        self.btnBox.rejected.connect(frmAddVectorLayer.reject)
        QtCore.QMetaObject.connectSlotsByName(frmAddVectorLayer)
        frmAddVectorLayer.setTabOrder(self.rdoFile, self.rdoDirectory)
        frmAddVectorLayer.setTabOrder(self.rdoDirectory, self.rdoDatabase)
        frmAddVectorLayer.setTabOrder(self.rdoDatabase, self.rdoProtocol)
        frmAddVectorLayer.setTabOrder(self.rdoProtocol, self.cboEncoding)
        frmAddVectorLayer.setTabOrder(self.cboEncoding, self.txtDataset)
        frmAddVectorLayer.setTabOrder(self.txtDataset, self.btnBrowse)
        frmAddVectorLayer.setTabOrder(self.btnBrowse, self.btnBox)

    def retranslateUi(self, frmAddVectorLayer):
        frmAddVectorLayer.setWindowTitle(_translate("frmAddVectorLayer", "Add vector layer", None))
        self.groupBox.setTitle(_translate("frmAddVectorLayer", "Source type", None))
        self.rdoDirectory.setText(_translate("frmAddVectorLayer", "Directory", None))
        self.rdoDatabase.setText(_translate("frmAddVectorLayer", "Database", None))
        self.lblEncoding.setText(_translate("frmAddVectorLayer", "Encoding", None))
        self.rdoFile.setText(_translate("frmAddVectorLayer", "File", None))
        self.rdoProtocol.setText(_translate("frmAddVectorLayer", "Protocol", None))
        self.groupBox_2.setTitle(_translate("frmAddVectorLayer", "Source", None))
        self.lblDataset.setText(_translate("frmAddVectorLayer", "Dataset", None))
        self.btnBrowse.setText(_translate("frmAddVectorLayer", "Browse", None))
        self.actionBtnBox_Clicked.setText(_translate("frmAddVectorLayer", "Confirm", None))
        self.actionBtnBox_Clicked.setToolTip(_translate("frmAddVectorLayer", "Confirm selection", None))
        self.actionBrowse_Clicked.setText(_translate("frmAddVectorLayer", "Browse", None))
        self.actionBrowse_Clicked.setToolTip(_translate("frmAddVectorLayer", "Browse for dataset", None))

