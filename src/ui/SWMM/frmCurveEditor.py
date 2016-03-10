import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
import core.swmm.curves
from ui.SWMM.frmCurveEditorDesigner import Ui_frmCurveEditor
import ui.convenience
from core.swmm.curves import CurveType
# from PyQt4.QtGui import *


class frmCurveEditor(QtGui.QMainWindow, Ui_frmCurveEditor):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cboCurveType.clear()
        ui.convenience.set_combo_items(core.swmm.curves.CurveType, self.cboCurveType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # QtCore.QObject.connect(self.cboCurveType, QtCore.SIGNAL("clicked()"), self.cboCurveType_currentIndexChanged)
        self.cboCurveType.currentIndexChanged.connect(self.cboCurveType_currentIndexChanged)
        # self.set_from(parent.project)   # do after init to set curve type
        self._parent = parent
        self.curve_type = ""

    def set_from(self, project, curve_type):
        # section = core.epanet.project.Control()
        self.curve_type = curve_type
        # section = core.epanet.project.Curves()
        section = project.find_section("CURVES")
        # curve_list = section.value[0:]
        # # assume we want to edit the first one
        # for curve in curve_list:
        #     if curve.curve_id == '1':
        #         self.txtCurveID.setText(str(curve.curve_id))
        #         self.txtDescription.setText(str(curve.description))
        #         ui.convenience.set_combo(self.cboCurveType, curve.curve_type)
        #         point_count = -1
        #         for point in curve.curve_xy:
        #             point_count += 1
        #             led = QtGui.QLineEdit(str(point[0]))
        #             self.tblMult.setItem(point_count,0,QtGui.QTableWidgetItem(led.text()))
        #             led = QtGui.QLineEdit(str(point[1]))
        #             self.tblMult.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))
        #         self.lblEquation.setText("Equation: ")

    def cmdOK_Clicked(self):
        # TODO: Check for duplicate curve ID
        # TODO: Check if X-values are in ascending order
        # TODO: Check for legal pump curve
        section = self._parent.project.find_section("CURVES")
        curve_list = section.value[0:]
        # assume we are editing the first one
        for curve in curve_list:
            if curve.curve_id == '1':
                curve.curve_id = self.txtCurveID.text()
                curve.description = self.txtDescription.text()
                curve.curve_type = core.swmm.curves.CurveType[self.cboCurveType.currentText()]
                curve.curve_xy = []
                for row in range(self.tblMult.rowCount()):
                    if self.tblMult.item(row,0) and self.tblMult.item(row,1):
                        x = self.tblMult.item(row,0).text()
                        y = self.tblMult.item(row,1).text()
                        if len(x) > 0 and len(y) > 0:
                            curve.curve_xy.append((x, y))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboCurveType_currentIndexChanged(self, newIndex):
        curve_type = core.swmm.curves.CurveType[self.cboCurveType.currentText()]
        if curve_type == CurveType.PUMP:
            self.tblMult.setHorizontalHeaderLabels(("Flow", "Head"))
        elif curve_type == CurveType.EFFICIENCY:
            self.tblMult.setHorizontalHeaderLabels(("Flow", "Efficiency"))
        elif curve_type == CurveType.HEADLOSS:
            self.tblMult.setHorizontalHeaderLabels(("Flow", "Headloss"))
        elif curve_type == CurveType.VOLUME:
            self.tblMult.setHorizontalHeaderLabels(("Height", "Volume"))

