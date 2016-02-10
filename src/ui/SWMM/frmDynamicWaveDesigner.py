# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmDynamicWave.ui'
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

class Ui_frmDynamicWave(object):
    def setupUi(self, frmDynamicWave):
        frmDynamicWave.setObjectName(_fromUtf8("frmDynamicWave"))
        frmDynamicWave.resize(395, 467)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmDynamicWave.setFont(font)
        self.centralWidget = QtGui.QWidget(frmDynamicWave)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(110, 430, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(210, 430, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.lblInertial = QtGui.QLabel(self.centralWidget)
        self.lblInertial.setGeometry(QtCore.QRect(30, 20, 141, 16))
        self.lblInertial.setObjectName(_fromUtf8("lblInertial"))
        self.cboInertial = QtGui.QComboBox(self.centralWidget)
        self.cboInertial.setGeometry(QtCore.QRect(210, 20, 151, 22))
        self.cboInertial.setObjectName(_fromUtf8("cboInertial"))
        self.lblNormal = QtGui.QLabel(self.centralWidget)
        self.lblNormal.setGeometry(QtCore.QRect(30, 60, 141, 16))
        self.lblNormal.setObjectName(_fromUtf8("lblNormal"))
        self.cboNormal = QtGui.QComboBox(self.centralWidget)
        self.cboNormal.setGeometry(QtCore.QRect(210, 60, 151, 22))
        self.cboNormal.setObjectName(_fromUtf8("cboNormal"))
        self.lblForce = QtGui.QLabel(self.centralWidget)
        self.lblForce.setGeometry(QtCore.QRect(30, 100, 141, 16))
        self.lblForce.setObjectName(_fromUtf8("lblForce"))
        self.cboForce = QtGui.QComboBox(self.centralWidget)
        self.cboForce.setGeometry(QtCore.QRect(210, 100, 151, 22))
        self.cboForce.setObjectName(_fromUtf8("cboForce"))
        self.cbxUseVariable = QtGui.QCheckBox(self.centralWidget)
        self.cbxUseVariable.setGeometry(QtCore.QRect(30, 150, 171, 17))
        self.cbxUseVariable.setObjectName(_fromUtf8("cbxUseVariable"))
        self.lblAdjusted = QtGui.QLabel(self.centralWidget)
        self.lblAdjusted.setGeometry(QtCore.QRect(220, 150, 81, 16))
        self.lblAdjusted.setObjectName(_fromUtf8("lblAdjusted"))
        self.lblPercent = QtGui.QLabel(self.centralWidget)
        self.lblPercent.setGeometry(QtCore.QRect(360, 150, 81, 16))
        self.lblPercent.setObjectName(_fromUtf8("lblPercent"))
        self.sbxAdjusted = QtGui.QSpinBox(self.centralWidget)
        self.sbxAdjusted.setGeometry(QtCore.QRect(310, 150, 42, 22))
        self.sbxAdjusted.setObjectName(_fromUtf8("sbxAdjusted"))
        self.lblMinimum = QtGui.QLabel(self.centralWidget)
        self.lblMinimum.setGeometry(QtCore.QRect(30, 190, 211, 16))
        self.lblMinimum.setObjectName(_fromUtf8("lblMinimum"))
        self.txtMinimum = QtGui.QLineEdit(self.centralWidget)
        self.txtMinimum.setGeometry(QtCore.QRect(282, 190, 81, 20))
        self.txtMinimum.setObjectName(_fromUtf8("txtMinimum"))
        self.lblTimeStep = QtGui.QLabel(self.centralWidget)
        self.lblTimeStep.setGeometry(QtCore.QRect(30, 230, 251, 16))
        self.lblTimeStep.setObjectName(_fromUtf8("lblTimeStep"))
        self.txtLengthening = QtGui.QLineEdit(self.centralWidget)
        self.txtLengthening.setGeometry(QtCore.QRect(280, 230, 81, 20))
        self.txtLengthening.setObjectName(_fromUtf8("txtLengthening"))
        self.lblSurface = QtGui.QLabel(self.centralWidget)
        self.lblSurface.setGeometry(QtCore.QRect(30, 270, 251, 16))
        self.lblSurface.setObjectName(_fromUtf8("lblSurface"))
        self.txtSurfaceArea = QtGui.QLineEdit(self.centralWidget)
        self.txtSurfaceArea.setGeometry(QtCore.QRect(280, 270, 81, 20))
        self.txtSurfaceArea.setObjectName(_fromUtf8("txtSurfaceArea"))
        self.lblMaximum = QtGui.QLabel(self.centralWidget)
        self.lblMaximum.setGeometry(QtCore.QRect(30, 310, 251, 16))
        self.lblMaximum.setObjectName(_fromUtf8("lblMaximum"))
        self.sbxTrials = QtGui.QSpinBox(self.centralWidget)
        self.sbxTrials.setGeometry(QtCore.QRect(280, 310, 81, 22))
        self.sbxTrials.setObjectName(_fromUtf8("sbxTrials"))
        self.lblHead = QtGui.QLabel(self.centralWidget)
        self.lblHead.setGeometry(QtCore.QRect(30, 350, 251, 16))
        self.lblHead.setObjectName(_fromUtf8("lblHead"))
        self.lblThreads = QtGui.QLabel(self.centralWidget)
        self.lblThreads.setGeometry(QtCore.QRect(30, 390, 251, 16))
        self.lblThreads.setObjectName(_fromUtf8("lblThreads"))
        self.cboThreads = QtGui.QComboBox(self.centralWidget)
        self.cboThreads.setGeometry(QtCore.QRect(210, 390, 151, 22))
        self.cboThreads.setObjectName(_fromUtf8("cboThreads"))
        self.txtTolerance = QtGui.QLineEdit(self.centralWidget)
        self.txtTolerance.setGeometry(QtCore.QRect(280, 350, 81, 20))
        self.txtTolerance.setObjectName(_fromUtf8("txtTolerance"))
        frmDynamicWave.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmDynamicWave)
        QtCore.QMetaObject.connectSlotsByName(frmDynamicWave)

    def retranslateUi(self, frmDynamicWave):
        frmDynamicWave.setWindowTitle(_translate("frmDynamicWave", "SWMM Dynamic Wave Options", None))
        self.cmdOK.setText(_translate("frmDynamicWave", "OK", None))
        self.cmdCancel.setText(_translate("frmDynamicWave", "Cancel", None))
        self.lblInertial.setText(_translate("frmDynamicWave", "Inertial Terms", None))
        self.lblNormal.setText(_translate("frmDynamicWave", "Normal Flow Criterion", None))
        self.lblForce.setText(_translate("frmDynamicWave", "Force Main Equation", None))
        self.cbxUseVariable.setText(_translate("frmDynamicWave", "Use Variable Time Steps", None))
        self.lblAdjusted.setText(_translate("frmDynamicWave", "Adjusted By", None))
        self.lblPercent.setText(_translate("frmDynamicWave", "%", None))
        self.lblMinimum.setText(_translate("frmDynamicWave", "Minimum Variable Time Step (sec)", None))
        self.lblTimeStep.setText(_translate("frmDynamicWave", "Time Step for Conduit Lengthening (sec)", None))
        self.lblSurface.setText(_translate("frmDynamicWave", "Minimum Nodal Surface Area (sq feet)", None))
        self.lblMaximum.setText(_translate("frmDynamicWave", "Maximum Trials Per Time Step", None))
        self.lblHead.setText(_translate("frmDynamicWave", "Head Convergence Tolerance (feet)", None))
        self.lblThreads.setText(_translate("frmDynamicWave", "Number of Threads", None))

