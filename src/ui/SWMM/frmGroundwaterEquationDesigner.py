# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmGroundwaterEquationDesigner.ui'
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

class Ui_frmGroundwaterEquation(object):
    def setupUi(self, frmGroundwaterEquation):
        frmGroundwaterEquation.setObjectName(_fromUtf8("frmGroundwaterEquation"))
        frmGroundwaterEquation.resize(541, 492)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmGroundwaterEquation.setFont(font)
        self.centralWidget = QtGui.QWidget(frmGroundwaterEquation)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraTop = QtGui.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.verticalLayout = QtGui.QVBoxLayout(self.fraTop)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtTop = QtGui.QLabel(self.fraTop)
        self.txtTop.setWordWrap(True)
        self.txtTop.setObjectName(_fromUtf8("txtTop"))
        self.verticalLayout.addWidget(self.txtTop)
        self.txtControls = QtGui.QPlainTextEdit(self.fraTop)
        self.txtControls.setObjectName(_fromUtf8("txtControls"))
        self.verticalLayout.addWidget(self.txtControls)
        self.textEdit = QtGui.QTextEdit(self.fraTop)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.verticalLayout_2.addWidget(self.fraTop)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(338, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtGui.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmGroundwaterEquation.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmGroundwaterEquation)
        QtCore.QMetaObject.connectSlotsByName(frmGroundwaterEquation)

    def retranslateUi(self, frmGroundwaterEquation):
        frmGroundwaterEquation.setWindowTitle(_translate("frmGroundwaterEquation", "SWMM Groundwater Flow Equation Editor", None))
        self.txtTop.setText(_translate("frmGroundwaterEquation", "Enter an expression to use in addition to the standard equation for lateral groundwater flow (leave blank to use only the standard equation):", None))
        self.textEdit.setHtml(_translate("frmGroundwaterEquation", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The result of evaluating your custom equation will be added onto the result of the standard equation. To replace the standard equation completely set all of its coefficients to 0. Remember that groundwater flow units are cfs/acre for US units and cms/ha for metric units.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can use the following symbols in your expression:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Hgw    (height of the groundwater table above aquifer bottom, ft or m)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Hsw    (height of the surface water above aquifer bottom, ft or m)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Hcb    (height of the channel bottom above aquifer bottom, ft or m)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Hgs    (height of the ground surface above aquifer bottom, ft or m)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Ks    (saturated hydraulic conductivity, in/hr or mm/hr)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  K    (unsaturated hydraulic conductivity, in/hr or mm/hr)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Theta    (moisture content of unsaturated upper zone, fraction)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Phi    (soil porosity, fraction)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Fi    (surface infiltration rate, in/hr or mm/hr)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Fu    (upper soil zone percolation rate, in/hr or mm/hr)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  A    (subcatchment area, ac or ha)</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Use the STEP function to have flow only when the groundwater level is above a certain threshold. For example, the expression:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    0.001 * (Hgw - 5) * STEP(Hgw - 5)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">would generate flow only when Hgw was above 5.</p></body></html>", None))
        self.cmdOK.setText(_translate("frmGroundwaterEquation", "OK", None))
        self.cmdCancel.setText(_translate("frmGroundwaterEquation", "Cancel", None))

