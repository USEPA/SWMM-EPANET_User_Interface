# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmGroundwaterFlowDesigner.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_frmGroundwaterFlow(object):
    def setupUi(self, frmGroundwaterFlow):
        frmGroundwaterFlow.setObjectName(_fromUtf8("frmGroundwaterFlow"))
        frmGroundwaterFlow.resize(680, 464)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmGroundwaterFlow.sizePolicy().hasHeightForWidth())
        frmGroundwaterFlow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmGroundwaterFlow.setFont(font)
        self.centralWidget = QtGui.QWidget(frmGroundwaterFlow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_6.setMargin(11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.fraLeft = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraLeft.sizePolicy().hasHeightForWidth())
        self.fraLeft.setSizePolicy(sizePolicy)
        self.fraLeft.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraLeft.setFrameShadow(QtGui.QFrame.Raised)
        self.fraLeft.setObjectName(_fromUtf8("fraLeft"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.fraLeft)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraTop = QtGui.QFrame(self.fraLeft)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraTop.sizePolicy().hasHeightForWidth())
        self.fraTop.setSizePolicy(sizePolicy)
        self.fraTop.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.fraTop)
        self.horizontalLayout_4.setMargin(11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.tblGeneric = QtGui.QTableWidget(self.fraTop)
        self.tblGeneric.setObjectName(_fromUtf8("tblGeneric"))
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblGeneric.setHorizontalHeaderItem(0, item)
        self.horizontalLayout_4.addWidget(self.tblGeneric)
        self.verticalLayout_2.addWidget(self.fraTop)
        self.fraNotes = QtGui.QFrame(self.fraLeft)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraNotes.sizePolicy().hasHeightForWidth())
        self.fraNotes.setSizePolicy(sizePolicy)
        self.fraNotes.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraNotes.setFrameShadow(QtGui.QFrame.Raised)
        self.fraNotes.setObjectName(_fromUtf8("fraNotes"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.fraNotes)
        self.horizontalLayout_5.setMargin(11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lblNotes = QtGui.QLabel(self.fraNotes)
        self.lblNotes.setWordWrap(True)
        self.lblNotes.setObjectName(_fromUtf8("lblNotes"))
        self.horizontalLayout_5.addWidget(self.lblNotes)
        self.verticalLayout_2.addWidget(self.fraNotes)
        self.horizontalLayout_6.addWidget(self.fraLeft)
        self.fraRight = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraRight.sizePolicy().hasHeightForWidth())
        self.fraRight.setSizePolicy(sizePolicy)
        self.fraRight.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraRight.setFrameShadow(QtGui.QFrame.Raised)
        self.fraRight.setObjectName(_fromUtf8("fraRight"))
        self.verticalLayout = QtGui.QVBoxLayout(self.fraRight)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraImage = QtGui.QFrame(self.fraRight)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraImage.sizePolicy().hasHeightForWidth())
        self.fraImage.setSizePolicy(sizePolicy)
        self.fraImage.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraImage.setFrameShadow(QtGui.QFrame.Raised)
        self.fraImage.setObjectName(_fromUtf8("fraImage"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraImage)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblImage = QtGui.QLabel(self.fraImage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblImage.sizePolicy().hasHeightForWidth())
        self.lblImage.setSizePolicy(sizePolicy)
        self.lblImage.setText(_fromUtf8(""))
        self.lblImage.setPixmap(QtGui.QPixmap(_fromUtf8("../swmmimages/gw.png")))
        self.lblImage.setObjectName(_fromUtf8("lblImage"))
        self.horizontalLayout.addWidget(self.lblImage)
        self.verticalLayout.addWidget(self.fraImage)
        self.fraText = QtGui.QFrame(self.fraRight)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraText.sizePolicy().hasHeightForWidth())
        self.fraText.setSizePolicy(sizePolicy)
        self.fraText.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraText.setFrameShadow(QtGui.QFrame.Raised)
        self.fraText.setObjectName(_fromUtf8("fraText"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.fraText)
        self.horizontalLayout_3.setMargin(11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.txtText = QtGui.QTextBrowser(self.fraText)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtText.sizePolicy().hasHeightForWidth())
        self.txtText.setSizePolicy(sizePolicy)
        self.txtText.setMinimumSize(QtCore.QSize(320, 0))
        self.txtText.setObjectName(_fromUtf8("txtText"))
        self.horizontalLayout_3.addWidget(self.txtText)
        self.verticalLayout.addWidget(self.fraText)
        self.fraOKCancel = QtGui.QFrame(self.fraRight)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraOKCancel.sizePolicy().hasHeightForWidth())
        self.fraOKCancel.setSizePolicy(sizePolicy)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(120, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cmdOK = QtGui.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout_2.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout_2.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        self.horizontalLayout_6.addWidget(self.fraRight)
        frmGroundwaterFlow.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmGroundwaterFlow)
        QtCore.QMetaObject.connectSlotsByName(frmGroundwaterFlow)

    def retranslateUi(self, frmGroundwaterFlow):
        frmGroundwaterFlow.setWindowTitle(_translate("frmGroundwaterFlow", "SWMM Groundwater Flow Editor", None))
        item = self.tblGeneric.horizontalHeaderItem(0)
        item.setText(_translate("frmGroundwaterFlow", "Value", None))
        self.lblNotes.setText(_translate("frmGroundwaterFlow", "Explanatory notes", None))
        self.txtText.setHtml(_translate("frmGroundwaterFlow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">The standard equation for lateral groundwater flow is:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">    QL  =  A1 * (Hgw - Hcb)^B1 </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">           - A2 * (Hsw - Hcb)^B2</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">           + A3 * Hgw * Hsw</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">where QL has units of cfs/ac (or cms/ha).</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">The standard equation for deep groundwater flow is:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">    QD  =  LGLR * Hgw / Hgs </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">where LGLR is the aquifer lower GW loss rate (in/hr or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">mm/hr).</span></p></body></html>", None))
        self.cmdOK.setText(_translate("frmGroundwaterFlow", "OK", None))
        self.cmdCancel.setText(_translate("frmGroundwaterFlow", "Cancel", None))

