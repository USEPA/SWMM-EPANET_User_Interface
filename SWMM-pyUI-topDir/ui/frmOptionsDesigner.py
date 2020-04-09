# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmOptionsDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_diagOptions(object):
    def setupUi(self, diagOptions):
        diagOptions.setObjectName("diagOptions")
        diagOptions.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(diagOptions)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableOptions = QtWidgets.QTreeWidget(diagOptions)
        self.tableOptions.setObjectName("tableOptions")
        self.verticalLayout.addWidget(self.tableOptions)
        self.buttonBox = QtWidgets.QDialogButtonBox(diagOptions)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(diagOptions)
        self.buttonBox.accepted.connect(diagOptions.accept)
        self.buttonBox.rejected.connect(diagOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(diagOptions)

    def retranslateUi(self, diagOptions):
        _translate = QtCore.QCoreApplication.translate
        diagOptions.setWindowTitle(_translate("diagOptions", "Options"))
        self.tableOptions.headerItem().setText(0, _translate("diagOptions", "Option"))
        self.tableOptions.headerItem().setText(1, _translate("diagOptions", "Value"))

