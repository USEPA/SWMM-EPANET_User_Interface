# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmTranslateCoordinatesDesigner.ui'
#
# Created: Thu Apr 20 22:51:35 2017
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

class Ui_frmTranslateCoordinatesDesigner(object):
    def setupUi(self, frmTranslateCoordinatesDesigner):
        frmTranslateCoordinatesDesigner.setObjectName(_fromUtf8("frmTranslateCoordinatesDesigner"))
        frmTranslateCoordinatesDesigner.resize(484, 253)
        self.gridLayout_3 = QtGui.QGridLayout(frmTranslateCoordinatesDesigner)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gbLL = QtGui.QGroupBox(frmTranslateCoordinatesDesigner)
        self.gbLL.setObjectName(_fromUtf8("gbLL"))
        self.gridLayout = QtGui.QGridLayout(self.gbLL)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblLL_src_x = QtGui.QLabel(self.gbLL)
        self.lblLL_src_x.setObjectName(_fromUtf8("lblLL_src_x"))
        self.gridLayout.addWidget(self.lblLL_src_x, 0, 0, 1, 1)
        self.txtLL_src_x = QtGui.QLineEdit(self.gbLL)
        self.txtLL_src_x.setObjectName(_fromUtf8("txtLL_src_x"))
        self.gridLayout.addWidget(self.txtLL_src_x, 0, 1, 1, 1)
        self.lblLL_dst_x = QtGui.QLabel(self.gbLL)
        self.lblLL_dst_x.setObjectName(_fromUtf8("lblLL_dst_x"))
        self.gridLayout.addWidget(self.lblLL_dst_x, 0, 2, 1, 1)
        self.txtLL_dst_x = QtGui.QLineEdit(self.gbLL)
        self.txtLL_dst_x.setObjectName(_fromUtf8("txtLL_dst_x"))
        self.gridLayout.addWidget(self.txtLL_dst_x, 0, 3, 1, 1)
        self.lblLL_src_y = QtGui.QLabel(self.gbLL)
        self.lblLL_src_y.setObjectName(_fromUtf8("lblLL_src_y"))
        self.gridLayout.addWidget(self.lblLL_src_y, 1, 0, 1, 1)
        self.txtLL_src_y = QtGui.QLineEdit(self.gbLL)
        self.txtLL_src_y.setObjectName(_fromUtf8("txtLL_src_y"))
        self.gridLayout.addWidget(self.txtLL_src_y, 1, 1, 1, 1)
        self.lblLL_dst_y = QtGui.QLabel(self.gbLL)
        self.lblLL_dst_y.setObjectName(_fromUtf8("lblLL_dst_y"))
        self.gridLayout.addWidget(self.lblLL_dst_y, 1, 2, 1, 1)
        self.txtLL_dst_y = QtGui.QLineEdit(self.gbLL)
        self.txtLL_dst_y.setObjectName(_fromUtf8("txtLL_dst_y"))
        self.gridLayout.addWidget(self.txtLL_dst_y, 1, 3, 1, 1)
        self.gridLayout_3.addWidget(self.gbLL, 0, 0, 1, 5)
        self.gb_UR = QtGui.QGroupBox(frmTranslateCoordinatesDesigner)
        self.gb_UR.setObjectName(_fromUtf8("gb_UR"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gb_UR)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblUR_src_x = QtGui.QLabel(self.gb_UR)
        self.lblUR_src_x.setObjectName(_fromUtf8("lblUR_src_x"))
        self.gridLayout_2.addWidget(self.lblUR_src_x, 0, 0, 1, 1)
        self.txtUR_src_x = QtGui.QLineEdit(self.gb_UR)
        self.txtUR_src_x.setObjectName(_fromUtf8("txtUR_src_x"))
        self.gridLayout_2.addWidget(self.txtUR_src_x, 0, 1, 1, 1)
        self.lblUR_dst_x = QtGui.QLabel(self.gb_UR)
        self.lblUR_dst_x.setObjectName(_fromUtf8("lblUR_dst_x"))
        self.gridLayout_2.addWidget(self.lblUR_dst_x, 0, 2, 1, 1)
        self.txtUR_dst_x = QtGui.QLineEdit(self.gb_UR)
        self.txtUR_dst_x.setObjectName(_fromUtf8("txtUR_dst_x"))
        self.gridLayout_2.addWidget(self.txtUR_dst_x, 0, 3, 1, 1)
        self.lblUR_src_y = QtGui.QLabel(self.gb_UR)
        self.lblUR_src_y.setObjectName(_fromUtf8("lblUR_src_y"))
        self.gridLayout_2.addWidget(self.lblUR_src_y, 1, 0, 1, 1)
        self.txtUR_src_y = QtGui.QLineEdit(self.gb_UR)
        self.txtUR_src_y.setObjectName(_fromUtf8("txtUR_src_y"))
        self.gridLayout_2.addWidget(self.txtUR_src_y, 1, 1, 1, 1)
        self.lblUR_dst_y = QtGui.QLabel(self.gb_UR)
        self.lblUR_dst_y.setObjectName(_fromUtf8("lblUR_dst_y"))
        self.gridLayout_2.addWidget(self.lblUR_dst_y, 1, 2, 1, 1)
        self.txtUR_dst_y = QtGui.QLineEdit(self.gb_UR)
        self.txtUR_dst_y.setObjectName(_fromUtf8("txtUR_dst_y"))
        self.gridLayout_2.addWidget(self.txtUR_dst_y, 1, 3, 1, 1)
        self.gridLayout_3.addWidget(self.gb_UR, 1, 0, 1, 5)
        self.lblUnit = QtGui.QLabel(frmTranslateCoordinatesDesigner)
        self.lblUnit.setObjectName(_fromUtf8("lblUnit"))
        self.gridLayout_3.addWidget(self.lblUnit, 2, 0, 1, 1)
        self.rdoUnitFeet = QtGui.QRadioButton(frmTranslateCoordinatesDesigner)
        self.rdoUnitFeet.setObjectName(_fromUtf8("rdoUnitFeet"))
        self.gridLayout_3.addWidget(self.rdoUnitFeet, 2, 1, 1, 1)
        self.rdoUnitMeters = QtGui.QRadioButton(frmTranslateCoordinatesDesigner)
        self.rdoUnitMeters.setObjectName(_fromUtf8("rdoUnitMeters"))
        self.gridLayout_3.addWidget(self.rdoUnitMeters, 2, 2, 1, 1)
        self.chkAutoUpdate = QtGui.QCheckBox(frmTranslateCoordinatesDesigner)
        self.chkAutoUpdate.setObjectName(_fromUtf8("chkAutoUpdate"))
        self.gridLayout_3.addWidget(self.chkAutoUpdate, 2, 3, 1, 2)
        spacerItem = QtGui.QSpacerItem(96, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 3, 0, 1, 3)
        self.btnTranslate = QtGui.QPushButton(frmTranslateCoordinatesDesigner)
        self.btnTranslate.setObjectName(_fromUtf8("btnTranslate"))
        self.gridLayout_3.addWidget(self.btnTranslate, 3, 3, 1, 1)
        self.btnCancel = QtGui.QPushButton(frmTranslateCoordinatesDesigner)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridLayout_3.addWidget(self.btnCancel, 3, 4, 1, 1)

        self.retranslateUi(frmTranslateCoordinatesDesigner)
        QtCore.QMetaObject.connectSlotsByName(frmTranslateCoordinatesDesigner)

    def retranslateUi(self, frmTranslateCoordinatesDesigner):
        frmTranslateCoordinatesDesigner.setWindowTitle(_translate("frmTranslateCoordinatesDesigner", "Translate Model Coordinates", None))
        self.gbLL.setTitle(_translate("frmTranslateCoordinatesDesigner", "A point selected in the LOWER LEFT corner: specify current and destination coordinates", None))
        self.lblLL_src_x.setText(_translate("frmTranslateCoordinatesDesigner", "Current x-coordinate", None))
        self.lblLL_dst_x.setText(_translate("frmTranslateCoordinatesDesigner", "Destination x-coordinate", None))
        self.lblLL_src_y.setText(_translate("frmTranslateCoordinatesDesigner", "Current y-coordinate", None))
        self.lblLL_dst_y.setText(_translate("frmTranslateCoordinatesDesigner", "Destination y-coordinate", None))
        self.gb_UR.setTitle(_translate("frmTranslateCoordinatesDesigner", "A point selected in the UPPER RIGHT corner: specify current and destination coordinates", None))
        self.lblUR_src_x.setText(_translate("frmTranslateCoordinatesDesigner", "Current x-coordinate", None))
        self.lblUR_dst_x.setText(_translate("frmTranslateCoordinatesDesigner", "Destination x-coordinate", None))
        self.lblUR_src_y.setText(_translate("frmTranslateCoordinatesDesigner", "Current y-coordinate", None))
        self.lblUR_dst_y.setText(_translate("frmTranslateCoordinatesDesigner", "Destination y-coordinate", None))
        self.lblUnit.setText(_translate("frmTranslateCoordinatesDesigner", "Destination Coordinate Unit:", None))
        self.rdoUnitFeet.setText(_translate("frmTranslateCoordinatesDesigner", "Feet", None))
        self.rdoUnitMeters.setText(_translate("frmTranslateCoordinatesDesigner", "Meters", None))
        self.chkAutoUpdate.setText(_translate("frmTranslateCoordinatesDesigner", "Re-calculate length and area", None))
        self.btnTranslate.setText(_translate("frmTranslateCoordinatesDesigner", "Translate Coordinates", None))
        self.btnCancel.setText(_translate("frmTranslateCoordinatesDesigner", "Cancel", None))

