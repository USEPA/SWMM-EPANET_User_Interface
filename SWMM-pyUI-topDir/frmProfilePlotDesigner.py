# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmProfilePlotDesigner.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
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

class Ui_frmProfilePlot(object):
    def setupUi(self, frmProfilePlot):
        frmProfilePlot.setObjectName(_fromUtf8("frmProfilePlot"))
        frmProfilePlot.resize(395, 328)
        font = QFont()
        font.setPointSize(10)
        frmProfilePlot.setFont(font)
        self.centralWidget = QWidget(frmProfilePlot)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_4 = QVBoxLayout(self.centralWidget)
        # self.verticalLayout_4.setMargin(11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.horizontalLayout_3 = QHBoxLayout(self.fraTop)
        # self.horizontalLayout_3.setMargin(11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.fraLeft = QFrame(self.fraTop)
        self.fraLeft.setFrameShape(QFrame.StyledPanel)
        self.fraLeft.setFrameShadow(QFrame.Raised)
        self.fraLeft.setObjectName(_fromUtf8("fraLeft"))
        self.verticalLayout = QVBoxLayout(self.fraLeft)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbxCreate = QGroupBox(self.fraLeft)
        self.gbxCreate.setObjectName(_fromUtf8("gbxCreate"))
        self.verticalLayout_3 = QVBoxLayout(self.gbxCreate)
        # self.verticalLayout_3.setMargin(11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.lblStart = QLabel(self.gbxCreate)
        self.lblStart.setObjectName(_fromUtf8("lblStart"))
        self.verticalLayout_3.addWidget(self.lblStart)
        self.cboStart = QComboBox(self.gbxCreate)
        self.cboStart.setObjectName(_fromUtf8("cboStart"))
        self.verticalLayout_3.addWidget(self.cboStart)
        self.lblEnd = QLabel(self.gbxCreate)
        self.lblEnd.setObjectName(_fromUtf8("lblEnd"))
        self.verticalLayout_3.addWidget(self.lblEnd)
        self.cboEnd = QComboBox(self.gbxCreate)
        self.cboEnd.setObjectName(_fromUtf8("cboEnd"))
        self.verticalLayout_3.addWidget(self.cboEnd)
        self.cmdFind = QPushButton(self.gbxCreate)
        self.cmdFind.setObjectName(_fromUtf8("cmdFind"))
        self.verticalLayout_3.addWidget(self.cmdFind)
        self.verticalLayout.addWidget(self.gbxCreate)
        self.cmdUse = QPushButton(self.fraLeft)
        self.cmdUse.setObjectName(_fromUtf8("cmdUse"))
        self.verticalLayout.addWidget(self.cmdUse)
        self.cmdSave = QPushButton(self.fraLeft)
        self.cmdSave.setObjectName(_fromUtf8("cmdSave"))
        self.verticalLayout.addWidget(self.cmdSave)
        self.horizontalLayout_3.addWidget(self.fraLeft)
        self.gbxLinks = QGroupBox(self.fraTop)
        self.gbxLinks.setObjectName(_fromUtf8("gbxLinks"))
        self.verticalLayout_2 = QVBoxLayout(self.gbxLinks)
        # self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lstData = QListWidget(self.gbxLinks)
        self.lstData.setObjectName(_fromUtf8("lstData"))
        self.verticalLayout_2.addWidget(self.lstData)
        self.horizontalLayout_3.addWidget(self.gbxLinks)
        self.verticalLayout_4.addWidget(self.fraTop)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(338, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_4.addWidget(self.fraOKCancel)
        frmProfilePlot.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmProfilePlot)
        QtCore.QMetaObject.connectSlotsByName(frmProfilePlot)

    def retranslateUi(self, frmProfilePlot):
        frmProfilePlot.setWindowTitle(_translate("frmProfilePlot", "SWMM Profile Plot Selection", None))
        self.gbxCreate.setTitle(_translate("frmProfilePlot", "Create Profile", None))
        self.lblStart.setText(_translate("frmProfilePlot", "Start Node", None))
        self.lblEnd.setText(_translate("frmProfilePlot", "End Node", None))
        self.cmdFind.setText(_translate("frmProfilePlot", "Find Path", None))
        self.cmdUse.setText(_translate("frmProfilePlot", "Use Saved Profile", None))
        self.cmdSave.setText(_translate("frmProfilePlot", "Save Current Profile", None))
        self.gbxLinks.setTitle(_translate("frmProfilePlot", "Links in Profile", None))
        self.cmdOK.setText(_translate("frmProfilePlot", "OK", None))
        self.cmdCancel.setText(_translate("frmProfilePlot", "Cancel", None))

