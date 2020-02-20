# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui-py3qt5\src\ui\SWMM\frmAboutDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmAbout(object):
    def setupUi(self, frmAbout):
        frmAbout.setObjectName("frmAbout")
        frmAbout.resize(616, 503)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmAbout.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmAbout)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblSwmm = QtWidgets.QLabel(self.frame)
        self.lblSwmm.setObjectName("lblSwmm")
        self.verticalLayout.addWidget(self.lblSwmm)
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setObjectName("tabWidget")
        self.tabDescription = QtWidgets.QWidget()
        self.tabDescription.setObjectName("tabDescription")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabDescription)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblAbout = QtWidgets.QLabel(self.tabDescription)
        self.lblAbout.setWordWrap(True)
        self.lblAbout.setObjectName("lblAbout")
        self.verticalLayout_4.addWidget(self.lblAbout)
        self.tabWidget.addTab(self.tabDescription, "")
        self.tabDisclaimer = QtWidgets.QWidget()
        self.tabDisclaimer.setObjectName("tabDisclaimer")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabDisclaimer)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblAbout_2 = QtWidgets.QLabel(self.tabDisclaimer)
        self.lblAbout_2.setWordWrap(True)
        self.lblAbout_2.setObjectName("lblAbout_2")
        self.verticalLayout_3.addWidget(self.lblAbout_2)
        self.tabWidget.addTab(self.tabDisclaimer, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addWidget(self.frame)
        self.fraOKCancel = QtWidgets.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraOKCancel.setObjectName("fraOKCancel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.fraOKCancel)
        self.label.setLineWidth(0)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmAbout.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmAbout)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmAbout)

    def retranslateUi(self, frmAbout):
        _translate = QtCore.QCoreApplication.translate
        frmAbout.setWindowTitle(_translate("frmAbout", "About SWMM"))
        self.lblSwmm.setText(_translate("frmAbout", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#0000ff;\">Storm Water Management Model</span></p><p align=\"center\"><span style=\" font-weight:600; color:#000000;\">Version MTP6r2 (Python 3.7, PyQGIS 3.6.0, PyQt 5.11.3)</span></p><p align=\"center\"><span style=\" font-weight:600; color:#000000;\">SWMM Engine Version 5.1.013</span></p></body></html>"))
        self.lblAbout.setText(_translate("frmAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The EPA Storm Water Management Model (SWMM) is a dynamic rainfall-runoff-routing simulation model used for single event or long-term (continuous) simulation of runoff quantity and quality from primarily urban areas. The runoff component of SWMM operates on a collection of subcatchment areas that receive precipitation and generate runoff and pollutant loads. The routing portion of SWMM transports this runoff through a system of pipes, channels, storage/treatment devices, pumps, and regulators. SWMM tracks the quantity and quality of runoff generated within each subcatchment, and the flow rate, flow depth, and quality of water in each pipe and channel during a simulation period comprised of multiple time steps.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">EPA SWMM is public domain software that may be freely copied and distributed.</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDescription), _translate("frmAbout", "Description"))
        self.lblAbout_2.setText(_translate("frmAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This software is provided on an &quot;as-is&quot; basis. US EPA makes no representations or warranties of any kind and expressly disclaim all other warranties express or implied, including, without limitation, warranties of merchantability or fitness for a particular purpose. Although care has been used in preparing the software product, US EPA disclaims all liability for its accuracy or completeness, and the user shall be solely responsible for the selection, use, efficiency and suitability of the software product. Any person who uses this product does so at their sole risk and without liability to US EPA. US EPA shall have no liability to users for the infringement of proprietary rights by the software product or any portion thereof.</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDisclaimer), _translate("frmAbout", "Disclaimer"))
        self.label.setText(_translate("frmAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">National Risk Management Research Laboratory</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">U.S. Environmental Protection Agency</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Cincinnati, Ohio 45268</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://www.epa.gov/water-research/storm-water-management-model-swmm\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">https://www.epa.gov/water-research/storm-water-management-model-swmm</span></a></p></body></html>"))
        self.cmdOK.setText(_translate("frmAbout", "OK"))

