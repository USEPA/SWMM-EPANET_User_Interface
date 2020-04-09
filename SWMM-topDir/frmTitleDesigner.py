# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmTitleDesigner.ui'
#
# Created: Tue Mar 08 16:51:13 2016
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

class Ui_frmTitle(object):
    def setupUi(self, frmTitle):
        frmTitle.setObjectName(_fromUtf8("frmTitle"))
        frmTitle.resize(433, 145)
        font = QFont()
        font.setPointSize(10)
        frmTitle.setFont(font)
        self.centralWidget = QWidget(frmTitle)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblTitle = QLabel(self.centralWidget)
        font = QFont()
        font.setPointSize(10)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName(_fromUtf8("lblTitle"))
        self.gridLayout.addWidget(self.lblTitle, 0, 0, 1, 1)
        self.txtTitle = QPlainTextEdit(self.centralWidget)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.gridLayout.addWidget(self.txtTitle, 0, 1, 1, 1)
        self.frame = QFrame(self.centralWidget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(194, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.frame)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.frame)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.gridLayout.addWidget(self.frame, 1, 1, 1, 1)
        frmTitle.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTitle)
        QtCore.QMetaObject.connectSlotsByName(frmTitle)
        frmTitle.setTabOrder(self.txtTitle, self.cmdOK)
        frmTitle.setTabOrder(self.cmdOK, self.cmdCancel)

    def retranslateUi(self, frmTitle):
        frmTitle.setWindowTitle(_translate("frmTitle", "SWMM Title", None))
        self.lblTitle.setText(_translate("frmTitle", "Title:", None))
        self.cmdOK.setText(_translate("frmTitle", "OK", None))
        self.cmdCancel.setText(_translate("frmTitle", "Cancel", None))

