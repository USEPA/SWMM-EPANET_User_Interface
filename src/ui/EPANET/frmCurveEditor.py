import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.curves
from ui.EPANET.frmCurveEditorDesigner import Ui_frmCurveEditor
import ui.convenience
from core.epanet.curves import CurveType
# from PyQt4.QtGui import *


class frmCurveEditor(QtGui.QMainWindow, Ui_frmCurveEditor):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.cboCurveType.clear()
        ui.convenience.set_combo_items(core.epanet.curves.CurveType, self.cboCurveType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # QtCore.QObject.connect(self.cboCurveType, QtCore.SIGNAL("clicked()"), self.cboCurveType_currentIndexChanged)
        self.cboCurveType.currentIndexChanged.connect(self.cboCurveType_currentIndexChanged)
        self.set_from(main_form.project, '1')
        self.selected_curve_id = '1'
        self._main_form = main_form

    def set_from(self, project, selected_curve_id):
        # section = core.epanet.project.Curves()
        section = project.find_section("CURVES")
        self.selected_curve_id = selected_curve_id
        curve_list = section.value[0:]
        # assume we want to edit the first one
        for curve in curve_list:
            if curve.curve_id == selected_curve_id:
                self.txtCurveID.setText(str(curve.curve_id))
                self.txtDescription.setText(str(curve.description))
                ui.convenience.set_combo(self.cboCurveType, curve.curve_type)
                point_count = -1
                for point in curve.curve_xy:
                    point_count += 1
                    led = QtGui.QLineEdit(str(point[0]))
                    self.tblMult.setItem(point_count, 0, QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(str(point[1]))
                    self.tblMult.setItem(point_count, 1, QtGui.QTableWidgetItem(led.text()))
                self.lblEquation.setText("Equation: ")

    def cmdOK_Clicked(self):
        # TODO: Check for duplicate curve ID
        # TODO: Check if X-values are in ascending order
        # TODO: Check for legal pump curve
        section = self._main_form.project.find_section("CURVES")
        curve_list = section.value[0:]
        for curve in curve_list:
            if curve.curve_id == self.selected_curve_id:
                curve.curve_id = self.txtCurveID.text()
                curve.description = self.txtDescription.text()
                curve.curve_type = core.epanet.curves.CurveType[self.cboCurveType.currentText()]
                curve.curve_xy = []
                for row in range(self.tblMult.rowCount()):
                    if self.tblMult.item(row,0) and self.tblMult.item(row,1):
                        x = self.tblMult.item(row, 0).text()
                        y = self.tblMult.item(row, 1).text()
                        if len(x) > 0 and len(y) > 0:
                            curve.curve_xy.append((x, y))
        self._main_form.list_objects()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboCurveType_currentIndexChanged(self, newIndex):
        curve_type = core.epanet.curves.CurveType[self.cboCurveType.currentText()]
        if curve_type == CurveType.PUMP:
            self.tblMult.setHorizontalHeaderLabels(("Flow", "Head"))
        elif curve_type == CurveType.EFFICIENCY:
            self.tblMult.setHorizontalHeaderLabels(("Flow", "Efficiency"))
        elif curve_type == CurveType.HEADLOSS:
            self.tblMult.setHorizontalHeaderLabels(("Flow", "Headloss"))
        elif curve_type == CurveType.VOLUME:
            self.tblMult.setHorizontalHeaderLabels(("Height", "Volume"))

    # def FitPumpCurve:
        # From Dcurve.pas, LR
        # Fits 1- or 3-point head curve data to power function
#
#     function TCurveForm.FitPumpCurve(var N: Integer): Boolean;
# //------------------------------------------------------
# // Fits 1- or 3-point head curve data to power function.
# //------------------------------------------------------
# var
#   h0, h1, h2 : Double;
#   h4, h5     : Double;
#   q0, q1, q2 : Double;
#   a, a1, b, c: Double;
#   I, Iter    : Integer;
# begin
#   if N = 1 then
#   begin
#     q0 := 0.0;
#     q1 := X[1];
#     h1 := Y[1];
#     h0 := 1.33334*h1;
#     q2 := 2.0*q1;
#     h2 := 0.0;
#   end
#   else
#   begin
#     q0 := X[1];
#     h0 := Y[1];
#     q1 := X[2];
#     h1 := Y[2];
#     q2 := X[3];
#     h2 := Y[3];
#   end;
#   a := h0;
#   b := 0.0;
#   c := 1.0;
#   if (h0 < TINY)
#   or (h0 - h1 < TINY)
#   or (h1 - h2 < TINY)
#   or (q1 - q0 < TINY)
#   or (q2 - q1 < TINY)
#   then Result := False
#   else
#   begin
#     a := h0;
#     Result := False;
#     for Iter := 1 to 5 do
#     begin
#       h4 := a - h1;
#       h5 := a - h2;
#       c := ln(h5/h4)/ln(q2/q1);
# {************************************************
#  NOTE: If c < 1.0 then pump curve is convex which
#        might cause convergence problems. This was
#        permitted in Version 1.x so it is kept the
#        same here. We might want to enforce c >= 1
#        in the future.
# *************************************************}
#       if (c <= 0.0) or (c > 20.0) then break;
#       b := -h4/Power(q1,c);
#       if b > 0.0 then break;
#       a1 := h0 - b*Power(q0,c);
#       if abs(a1 - a) < 0.01 then
#       begin
#         Result := True;
#         break;
#       end;
#       a := a1;
#     end;
#   end;
#   if Result = True then
#   begin
#     N := 25;
#     with CurveGrid do
#       if N > RowCount then N := RowCount;
#     h4 := -a/b;
#     h5 := 1.0/c;
#     q1 := Power(h4,h5);
#     q1 := q1/N;
#     X[1] := 0.0;
#     Y[1] := a;
#     for I := 2 to N do
#     begin
#       X[I] := (I-1)*q1;
#       Y[I] := a + b*Power(X[I],c);
#     end;
#     CurveEqn.Caption := Format(FMT_EQN,[a,b,c]);
#   end
#   else CurveEqn.Caption := TXT_BAD_CURVE;
#   EqnLabel.Enabled := True;
# end;
