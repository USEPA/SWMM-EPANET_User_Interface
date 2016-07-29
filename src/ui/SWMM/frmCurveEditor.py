import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
import core.swmm.curves
from ui.SWMM.frmCurveEditorDesigner import Ui_frmCurveEditor
import ui.convenience
from core.swmm.curves import CurveType
# from PyQt4.QtGui import *


class frmCurveEditor(QtGui.QMainWindow, Ui_frmCurveEditor):
    def __init__(self, main_form, title, curve_type):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/curveeditordialog.htm"
        self.setupUi(self)
        if title:
            self.setWindowTitle(title)
        self.cboCurveType.clear()
        ui.convenience.set_combo_items(core.swmm.curves.CurveType, self.cboCurveType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # QtCore.QObject.connect(self.cboCurveType, QtCore.SIGNAL("clicked()"), self.cboCurveType_currentIndexChanged)
        self.cboCurveType.currentIndexChanged.connect(self.cboCurveType_currentIndexChanged)
        # self.set_from(main_form.project)   # do after init to set curve type
        self._main_form = main_form
        self.curve_type = curve_type
        self.curve_name = ''
        if main_form and main_form.project and curve_type:
            self.set_from(main_form.project, self.curve_name)

    def set_from(self, project, curve_name):
        # section = core.swmm.project.Curves()
        section = project.find_section("CURVES")

        if self.curve_type == "CONTROL":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Controller Value","Control Setting"))
        elif self.curve_type == "DIVERSION":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Inflow (CFS)","Outflow (CFS)"))
        elif self.curve_type == "PUMP":
            self.cboCurveType.setVisible(True)
            self.lblCurveType.setVisible(True)
            self.tblMult.setHorizontalHeaderLabels(("Depth (ft)","Flow (CFS)"))
            self.cboCurveType.clear()
            self.cboCurveType.addItems(("TYPE1","TYPE2","TYPE3","TYPE4"))
        elif self.curve_type == "RATING":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Head (ft)","Outflow (CFS)"))
        elif self.curve_type == "SHAPE":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Depth/Full Depth","Width/Full Depth"))
        elif self.curve_type == "STORAGE":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Depth (ft)","Area (ft2)"))
        elif self.curve_type == "TIDAL":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Hour of Day","Stage (ft)"))

        curve_list = section.value[0:]
        for curve in curve_list:
            if curve.name == curve_name and curve.curve_type.name[:4] == self.curve_type[:4]:
                self.txtCurveID.setText(str(curve.name))
                # self.txtDescription.setText(str(curve.description))
                if self.curve_type == "PUMP":
                    if curve.curve_type.name == "PUMP1":
                        self.cboCurveType.setCurrentIndex(0)
                    if curve.curve_type.name == "PUMP2":
                        self.cboCurveType.setCurrentIndex(1)
                    if curve.curve_type.name == "PUMP3":
                        self.cboCurveType.setCurrentIndex(2)
                    if curve.curve_type.name == "PUMP4":
                        self.cboCurveType.setCurrentIndex(3)
                point_count = -1
                for point in curve.curve_xy:
                     point_count += 1
                     led = QtGui.QLineEdit(str(point[0]))
                     self.tblMult.setItem(point_count,0,QtGui.QTableWidgetItem(led.text()))
                     led = QtGui.QLineEdit(str(point[1]))
                     self.tblMult.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        # TODO: Check for blank/duplicate curve ID
        # TODO: Check if X-values are in ascending order
        section = self._main_form.project.curves
        curve_list = section.value[0:]
        # assume we are editing the first one
        for curve in curve_list:
            if curve.name == self.curve_name and curve.curve_type.name[:4] == self.curve_type[:4]:
                curve.name = self.txtCurveID.text()
                # curve.description = self.txtDescription.text()
                # curve.curve_type = core.swmm.curves.CurveType[self.cboCurveType.currentText()]
                if self.curve_type == "PUMP":
                    if self.cboCurveType.currentIndex() == 0:
                        curve.curve_type = core.swmm.curves.CurveType["PUMP1"]
                    if self.cboCurveType.currentIndex() == 1:
                        curve.curve_type = core.swmm.curves.CurveType["PUMP2"]
                    if self.cboCurveType.currentIndex() == 2:
                        curve.curve_type = core.swmm.curves.CurveType["PUMP3"]
                    if self.cboCurveType.currentIndex() == 3:
                        curve.curve_type = core.swmm.curves.CurveType["PUMP4"]
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
        curve_type = self.cboCurveType.currentText()
        if curve_type == "TYPE1":
            self.tblMult.setHorizontalHeaderLabels(("Volume (ft3)","Flow (CFS)"))
        elif curve_type == "TYPE2":
            self.tblMult.setHorizontalHeaderLabels(("Depth (ft)","Flow (CFS)"))
        elif curve_type == "TYPE3":
            self.tblMult.setHorizontalHeaderLabels(("Head (ft)","Flow (CFS)"))
        elif curve_type == "TYPE4":
            self.tblMult.setHorizontalHeaderLabels(("Depth (ft)","Flow (CFS)"))

