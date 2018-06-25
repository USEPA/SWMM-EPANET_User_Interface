# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmOptionsDesigner.ui'
#
# Created: Sat Jan 23 03:37:06 2016
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

class Ui_diagOptions(object):
    def setupUi(self, diagOptions):
        diagOptions.setObjectName(_fromUtf8("diagOptions"))
        diagOptions.resize(400, 300)
        self.verticalLayout = QVBoxLayout(diagOptions)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableOptions = QTreeWidget(diagOptions)
        self.tableOptions.setObjectName(_fromUtf8("tableOptions"))
        self.verticalLayout.addWidget(self.tableOptions)
        self.buttonBox = QDialogButtonBox(diagOptions)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(diagOptions)
        self.buttonBox.accepted.connect(diagOptions.accept)
        self.buttonBox.rejected.connect(diagOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(diagOptions)

    def retranslateUi(self, diagOptions):
        diagOptions.setWindowTitle(_translate("diagOptions", "Options", None))
        self.tableOptions.headerItem().setText(0, _translate("diagOptions", "Option", None))
        self.tableOptions.headerItem().setText(1, _translate("diagOptions", "Value", None))

