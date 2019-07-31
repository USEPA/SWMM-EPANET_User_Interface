# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmReportOptionsDesigner.ui'
#
# Created: Tue Mar 08 16:50:57 2016
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

class Ui_frmReportOptions(object):
    def setupUi(self, frmReportOptions):
        frmReportOptions.setObjectName(_fromUtf8("frmReportOptions"))
        frmReportOptions.resize(578, 364)
        font = QFont()
        font.setPointSize(10)
        frmReportOptions.setFont(font)
        self.centralWidget = QWidget(frmReportOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbxReport = QGroupBox(self.centralWidget)
        self.gbxReport.setObjectName(_fromUtf8("gbxReport"))
        self.horizontalLayout = QHBoxLayout(self.gbxReport)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cbxInput = QCheckBox(self.gbxReport)
        self.cbxInput.setObjectName(_fromUtf8("cbxInput"))
        self.horizontalLayout.addWidget(self.cbxInput)
        self.cbxContinuity = QCheckBox(self.gbxReport)
        self.cbxContinuity.setObjectName(_fromUtf8("cbxContinuity"))
        self.horizontalLayout.addWidget(self.cbxContinuity)
        self.cbxFlow = QCheckBox(self.gbxReport)
        self.cbxFlow.setObjectName(_fromUtf8("cbxFlow"))
        self.horizontalLayout.addWidget(self.cbxFlow)
        self.cbxControls = QCheckBox(self.gbxReport)
        self.cbxControls.setObjectName(_fromUtf8("cbxControls"))
        self.horizontalLayout.addWidget(self.cbxControls)
        self.verticalLayout.addWidget(self.gbxReport)
        self.fraObjects = QFrame(self.centralWidget)
        self.fraObjects.setFrameShape(QFrame.StyledPanel)
        self.fraObjects.setFrameShadow(QFrame.Raised)
        self.fraObjects.setObjectName(_fromUtf8("fraObjects"))
        self.horizontalLayout_3 = QHBoxLayout(self.fraObjects)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gbxNode = QGroupBox(self.fraObjects)
        self.gbxNode.setObjectName(_fromUtf8("gbxNode"))
        self.gridLayout = QGridLayout(self.gbxNode)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QListWidget(self.gbxNode)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 2)
        self.cmdNodeAll = QPushButton(self.gbxNode)
        self.cmdNodeAll.setObjectName(_fromUtf8("cmdNodeAll"))
        self.gridLayout.addWidget(self.cmdNodeAll, 1, 0, 1, 1)
        self.cmdNodeNone = QPushButton(self.gbxNode)
        self.cmdNodeNone.setObjectName(_fromUtf8("cmdNodeNone"))
        self.gridLayout.addWidget(self.cmdNodeNone, 1, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.gbxNode)
        self.gbxLinks = QGroupBox(self.fraObjects)
        self.gbxLinks.setObjectName(_fromUtf8("gbxLinks"))
        self.gridLayout_2 = QGridLayout(self.gbxLinks)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.listWidget_2 = QListWidget(self.gbxLinks)
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.gridLayout_2.addWidget(self.listWidget_2, 0, 0, 1, 2)
        self.cmdLinksAll = QPushButton(self.gbxLinks)
        self.cmdLinksAll.setObjectName(_fromUtf8("cmdLinksAll"))
        self.gridLayout_2.addWidget(self.cmdLinksAll, 1, 0, 1, 1)
        self.cmdLinksNone = QPushButton(self.gbxLinks)
        self.cmdLinksNone.setObjectName(_fromUtf8("cmdLinksNone"))
        self.gridLayout_2.addWidget(self.cmdLinksNone, 1, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.gbxLinks)
        self.gbxSubcatchments = QGroupBox(self.fraObjects)
        self.gbxSubcatchments.setObjectName(_fromUtf8("gbxSubcatchments"))
        self.gridLayout_3 = QGridLayout(self.gbxSubcatchments)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.listWidget_3 = QListWidget(self.gbxSubcatchments)
        self.listWidget_3.setObjectName(_fromUtf8("listWidget_3"))
        self.gridLayout_3.addWidget(self.listWidget_3, 0, 0, 1, 2)
        self.cmdSubcatchmentsAll = QPushButton(self.gbxSubcatchments)
        self.cmdSubcatchmentsAll.setObjectName(_fromUtf8("cmdSubcatchmentsAll"))
        self.gridLayout_3.addWidget(self.cmdSubcatchmentsAll, 1, 0, 1, 1)
        self.cmdSubcatchmentsNone = QPushButton(self.gbxSubcatchments)
        self.cmdSubcatchmentsNone.setObjectName(_fromUtf8("cmdSubcatchmentsNone"))
        self.gridLayout_3.addWidget(self.cmdSubcatchmentsNone, 1, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.gbxSubcatchments)
        self.verticalLayout.addWidget(self.fraObjects)
        self.fraButtons = QFrame(self.centralWidget)
        self.fraButtons.setFrameShape(QFrame.StyledPanel)
        self.fraButtons.setFrameShadow(QFrame.Raised)
        self.fraButtons.setObjectName(_fromUtf8("fraButtons"))
        self.horizontalLayout_2 = QHBoxLayout(self.fraButtons)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QSpacerItem(375, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraButtons)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout_2.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraButtons)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout_2.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraButtons)
        frmReportOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmReportOptions)
        QtCore.QMetaObject.connectSlotsByName(frmReportOptions)
        frmReportOptions.setTabOrder(self.cbxInput, self.cbxContinuity)
        frmReportOptions.setTabOrder(self.cbxContinuity, self.cbxFlow)
        frmReportOptions.setTabOrder(self.cbxFlow, self.cbxControls)
        frmReportOptions.setTabOrder(self.cbxControls, self.listWidget)
        frmReportOptions.setTabOrder(self.listWidget, self.cmdNodeAll)
        frmReportOptions.setTabOrder(self.cmdNodeAll, self.cmdNodeNone)
        frmReportOptions.setTabOrder(self.cmdNodeNone, self.listWidget_2)
        frmReportOptions.setTabOrder(self.listWidget_2, self.cmdLinksAll)
        frmReportOptions.setTabOrder(self.cmdLinksAll, self.cmdLinksNone)
        frmReportOptions.setTabOrder(self.cmdLinksNone, self.listWidget_3)
        frmReportOptions.setTabOrder(self.listWidget_3, self.cmdSubcatchmentsAll)
        frmReportOptions.setTabOrder(self.cmdSubcatchmentsAll, self.cmdSubcatchmentsNone)
        frmReportOptions.setTabOrder(self.cmdSubcatchmentsNone, self.cmdOK)
        frmReportOptions.setTabOrder(self.cmdOK, self.cmdCancel)

    def retranslateUi(self, frmReportOptions):
        frmReportOptions.setWindowTitle(_translate("frmReportOptions", "SWMM Report Options", None))
        self.gbxReport.setTitle(_translate("frmReportOptions", "Report Options", None))
        self.cbxInput.setText(_translate("frmReportOptions", "Input Summary", None))
        self.cbxContinuity.setText(_translate("frmReportOptions", "Continuity Checks", None))
        self.cbxFlow.setText(_translate("frmReportOptions", "Flow Stats", None))
        self.cbxControls.setText(_translate("frmReportOptions", "Controls", None))
        self.gbxNode.setTitle(_translate("frmReportOptions", "Nodes", None))
        self.cmdNodeAll.setText(_translate("frmReportOptions", "All", None))
        self.cmdNodeNone.setText(_translate("frmReportOptions", "None", None))
        self.gbxLinks.setTitle(_translate("frmReportOptions", "Links", None))
        self.cmdLinksAll.setText(_translate("frmReportOptions", "All", None))
        self.cmdLinksNone.setText(_translate("frmReportOptions", "None", None))
        self.gbxSubcatchments.setTitle(_translate("frmReportOptions", "Subcatchments", None))
        self.cmdSubcatchmentsAll.setText(_translate("frmReportOptions", "All", None))
        self.cmdSubcatchmentsNone.setText(_translate("frmReportOptions", "None", None))
        self.cmdOK.setText(_translate("frmReportOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmReportOptions", "Cancel", None))

