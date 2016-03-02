# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmOptionsDesigner.ui'
#
# Created: Sat Jan 23 03:37:06 2016
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_diagOptions(object):
    def setupUi(self, diagOptions):
        diagOptions.setObjectName(_fromUtf8("diagOptions"))
        diagOptions.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(diagOptions)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableOptions = QtGui.QTreeWidget(diagOptions)
        self.tableOptions.setObjectName(_fromUtf8("tableOptions"))
        self.verticalLayout.addWidget(self.tableOptions)
        self.buttonBox = QtGui.QDialogButtonBox(diagOptions)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(diagOptions)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), diagOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), diagOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(diagOptions)

    def retranslateUi(self, diagOptions):
        diagOptions.setWindowTitle(_translate("diagOptions", "Options", None))
        self.tableOptions.headerItem().setText(0, _translate("diagOptions", "Option", None))
        self.tableOptions.headerItem().setText(1, _translate("diagOptions", "Value", None))

