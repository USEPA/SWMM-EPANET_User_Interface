# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPANET\frmSummaryDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmSummary(object):
    def setupUi(self, frmSummary):
        frmSummary.setObjectName("frmSummary")
        frmSummary.resize(541, 433)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmSummary.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmSummary)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbxTitle = QtWidgets.QGroupBox(self.centralWidget)
        self.gbxTitle.setObjectName("gbxTitle")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.gbxTitle)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtTitle = QtWidgets.QLineEdit(self.gbxTitle)
        self.txtTitle.setObjectName("txtTitle")
        self.horizontalLayout_2.addWidget(self.txtTitle)
        self.verticalLayout.addWidget(self.gbxTitle)
        self.gbxNotes = QtWidgets.QGroupBox(self.centralWidget)
        self.gbxNotes.setObjectName("gbxNotes")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gbxNotes)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.txtNotes = QtWidgets.QPlainTextEdit(self.gbxNotes)
        self.txtNotes.setObjectName("txtNotes")
        self.verticalLayout_2.addWidget(self.txtNotes)
        self.verticalLayout.addWidget(self.gbxNotes)
        self.gbxStats = QtWidgets.QGroupBox(self.centralWidget)
        self.gbxStats.setObjectName("gbxStats")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gbxStats)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.txtStats = QtWidgets.QPlainTextEdit(self.gbxStats)
        self.txtStats.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.txtStats.setObjectName("txtStats")
        self.verticalLayout_3.addWidget(self.txtStats)
        self.verticalLayout.addWidget(self.gbxStats)
        self.fraOKCancel = QtWidgets.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraOKCancel.setObjectName("fraOKCancel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmSummary.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmSummary)
        QtCore.QMetaObject.connectSlotsByName(frmSummary)

    def retranslateUi(self, frmSummary):
        _translate = QtCore.QCoreApplication.translate
        frmSummary.setWindowTitle(_translate("frmSummary", "EPANET Project Summary"))
        self.gbxTitle.setTitle(_translate("frmSummary", "Title"))
        self.gbxNotes.setTitle(_translate("frmSummary", "Notes"))
        self.gbxStats.setTitle(_translate("frmSummary", "Statistics"))
        self.cmdOK.setText(_translate("frmSummary", "OK"))
        self.cmdCancel.setText(_translate("frmSummary", "Cancel"))

