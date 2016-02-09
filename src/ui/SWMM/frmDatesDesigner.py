# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmDates.ui'
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

class Ui_frmDates(object):
    def setupUi(self, frmDates):
        frmDates.setObjectName(_fromUtf8("frmDates"))
        frmDates.resize(401, 330)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmDates.setFont(font)
        self.centralWidget = QtGui.QWidget(frmDates)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(110, 290, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(220, 290, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.lblStart = QtGui.QLabel(self.centralWidget)
        self.lblStart.setGeometry(QtCore.QRect(40, 50, 101, 16))
        self.lblStart.setObjectName(_fromUtf8("lblStart"))
        self.lblStartReporting = QtGui.QLabel(self.centralWidget)
        self.lblStartReporting.setGeometry(QtCore.QRect(40, 90, 111, 16))
        self.lblStartReporting.setObjectName(_fromUtf8("lblStartReporting"))
        self.lblEnd = QtGui.QLabel(self.centralWidget)
        self.lblEnd.setGeometry(QtCore.QRect(40, 130, 101, 16))
        self.lblEnd.setObjectName(_fromUtf8("lblEnd"))
        self.lblStartSweeping = QtGui.QLabel(self.centralWidget)
        self.lblStartSweeping.setGeometry(QtCore.QRect(40, 170, 121, 16))
        self.lblStartSweeping.setObjectName(_fromUtf8("lblStartSweeping"))
        self.lblDays = QtGui.QLabel(self.centralWidget)
        self.lblDays.setGeometry(QtCore.QRect(170, 30, 101, 16))
        self.lblDays.setObjectName(_fromUtf8("lblDays"))
        self.lblTimes = QtGui.QLabel(self.centralWidget)
        self.lblTimes.setGeometry(QtCore.QRect(290, 30, 101, 16))
        self.lblTimes.setObjectName(_fromUtf8("lblTimes"))
        self.tmeStart = QtGui.QTimeEdit(self.centralWidget)
        self.tmeStart.setGeometry(QtCore.QRect(290, 50, 81, 22))
        self.tmeStart.setProperty("showGroupSeparator", False)
        self.tmeStart.setObjectName(_fromUtf8("tmeStart"))
        self.tmeReport = QtGui.QTimeEdit(self.centralWidget)
        self.tmeReport.setGeometry(QtCore.QRect(290, 90, 81, 22))
        self.tmeReport.setProperty("showGroupSeparator", False)
        self.tmeReport.setObjectName(_fromUtf8("tmeReport"))
        self.tmeEnd = QtGui.QTimeEdit(self.centralWidget)
        self.tmeEnd.setGeometry(QtCore.QRect(290, 130, 81, 22))
        self.tmeEnd.setProperty("showGroupSeparator", False)
        self.tmeEnd.setObjectName(_fromUtf8("tmeEnd"))
        self.dedStart = QtGui.QDateEdit(self.centralWidget)
        self.dedStart.setGeometry(QtCore.QRect(170, 50, 110, 22))
        self.dedStart.setDate(QtCore.QDate(2002, 1, 1))
        self.dedStart.setObjectName(_fromUtf8("dedStart"))
        self.dedStartReport = QtGui.QDateEdit(self.centralWidget)
        self.dedStartReport.setGeometry(QtCore.QRect(170, 90, 110, 22))
        self.dedStartReport.setDate(QtCore.QDate(2002, 1, 1))
        self.dedStartReport.setObjectName(_fromUtf8("dedStartReport"))
        self.dedEnd = QtGui.QDateEdit(self.centralWidget)
        self.dedEnd.setGeometry(QtCore.QRect(170, 130, 110, 22))
        self.dedEnd.setDate(QtCore.QDate(2002, 1, 1))
        self.dedEnd.setObjectName(_fromUtf8("dedEnd"))
        self.lblEndSweeping = QtGui.QLabel(self.centralWidget)
        self.lblEndSweeping.setGeometry(QtCore.QRect(40, 210, 121, 16))
        self.lblEndSweeping.setObjectName(_fromUtf8("lblEndSweeping"))
        self.lblAntecedent = QtGui.QLabel(self.centralWidget)
        self.lblAntecedent.setGeometry(QtCore.QRect(40, 250, 141, 16))
        self.lblAntecedent.setObjectName(_fromUtf8("lblAntecedent"))
        self.dedSweepStart = QtGui.QDateEdit(self.centralWidget)
        self.dedSweepStart.setGeometry(QtCore.QRect(170, 170, 81, 22))
        self.dedSweepStart.setObjectName(_fromUtf8("dedSweepStart"))
        self.dedSweepEnd = QtGui.QDateEdit(self.centralWidget)
        self.dedSweepEnd.setGeometry(QtCore.QRect(170, 210, 81, 22))
        self.dedSweepEnd.setObjectName(_fromUtf8("dedSweepEnd"))
        self.txtAntecedent = QtGui.QLineEdit(self.centralWidget)
        self.txtAntecedent.setGeometry(QtCore.QRect(170, 250, 81, 20))
        self.txtAntecedent.setObjectName(_fromUtf8("txtAntecedent"))
        frmDates.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmDates)
        QtCore.QMetaObject.connectSlotsByName(frmDates)

    def retranslateUi(self, frmDates):
        frmDates.setWindowTitle(_translate("frmDates", "SWMM Dates Options", None))
        self.cmdOK.setText(_translate("frmDates", "OK", None))
        self.cmdCancel.setText(_translate("frmDates", "Cancel", None))
        self.lblStart.setText(_translate("frmDates", "Start Analysis on", None))
        self.lblStartReporting.setText(_translate("frmDates", "Start Reporting on", None))
        self.lblEnd.setText(_translate("frmDates", "End Analysis on", None))
        self.lblStartSweeping.setText(_translate("frmDates", "Start Sweeping on", None))
        self.lblDays.setText(_translate("frmDates", "Date (M/D/Y)", None))
        self.lblTimes.setText(_translate("frmDates", "Time (H:M)", None))
        self.tmeStart.setDisplayFormat(_translate("frmDates", "hh:mm", None))
        self.tmeReport.setDisplayFormat(_translate("frmDates", "hh:mm", None))
        self.tmeEnd.setDisplayFormat(_translate("frmDates", "hh:mm", None))
        self.dedStart.setDisplayFormat(_translate("frmDates", "MM/dd/yyyy", None))
        self.dedStartReport.setDisplayFormat(_translate("frmDates", "MM/dd/yyyy", None))
        self.dedEnd.setDisplayFormat(_translate("frmDates", "MM/dd/yyyy", None))
        self.lblEndSweeping.setText(_translate("frmDates", "End Sweeping on", None))
        self.lblAntecedent.setText(_translate("frmDates", "Antecedent Dry Days", None))
        self.dedSweepStart.setDisplayFormat(_translate("frmDates", "MM/dd", None))
        self.dedSweepEnd.setDisplayFormat(_translate("frmDates", "MM/dd", None))

