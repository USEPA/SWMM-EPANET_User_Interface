# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmProgramDesigner.ui'
#
# Created: Mon Jan 25 01:59:23 2016
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

class Ui_program(object):
    def setupUi(self, program):
        program.setObjectName(_fromUtf8("program"))
        program.resize(259, 135)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        program.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icon_swmm.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        program.setWindowIcon(icon)
        program.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(program)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnSWMM = QtGui.QPushButton(program)
        self.btnSWMM.setMinimumSize(QtCore.QSize(184, 52))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnSWMM.setFont(font)
        self.btnSWMM.setIcon(icon)
        self.btnSWMM.setObjectName(_fromUtf8("btnSWMM"))
        self.verticalLayout.addWidget(self.btnSWMM)
        self.btnEPANET = QtGui.QPushButton(program)
        self.btnEPANET.setMinimumSize(QtCore.QSize(184, 52))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnEPANET.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icon_epanet.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEPANET.setIcon(icon1)
        self.btnEPANET.setObjectName(_fromUtf8("btnEPANET"))
        self.verticalLayout.addWidget(self.btnEPANET)

        self.retranslateUi(program)
        QtCore.QMetaObject.connectSlotsByName(program)

    def retranslateUi(self, program):
        program.setWindowTitle(_translate("program", "Program", None))
        self.btnSWMM.setText(_translate("program", "SWMM", None))
        self.btnEPANET.setText(_translate("program", "EPANET", None))

import swmm_rc
