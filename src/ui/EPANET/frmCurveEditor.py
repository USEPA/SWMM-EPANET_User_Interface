import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.curves
from ui.EPANET.frmCurveEditorDesigner import Ui_frmCurveEditor
import ui.convenience
from core.epanet.curves import CurveType
from core.epanet.curves import Curve
from PyQt4.QtGui import *
import numpy as np
from ui.model_utility import ParseData
from ui.model_utility import BasePlot
from math import isnan
import os
import traceback


class frmCurveEditor(QtGui.QMainWindow, Ui_frmCurveEditor):
    def __init__(self, main_form, edit_these, new_item):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Curve_Ed.htm"
        self.setupUi(self)
        self.loaded = False
        self.cboCurveType.clear()
        ui.convenience.set_combo_items(core.epanet.curves.CurveType, self.cboCurveType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        #QtCore.QObject.connect(self.tblMult, QtCore.SIGNAL("cellChanged(int, int)"), self.tblMult_cellChanged(int, int))
        #QtCore.QObject.connect(self.cboCurveType, QtCore.SIGNAL("clicked()"), self.cboCurveType_currentIndexChanged)
        self.cboCurveType.currentIndexChanged.connect(self.cboCurveType_currentIndexChanged)
        self.btnSave.clicked.connect(self.save_curve_data)
        self.btnLoad.clicked.connect(self.load_curve_data)
        self.tblMult.cellChanged.connect(self.tblMult_cellChanged)
        self.selected_curve_name = ''
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.curves
        self.plot = CurvePlot(self.fraPlot, width=6, height=2, dpi=100)
        layout = QtGui.QVBoxLayout(self.fraPlot)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot)
        self.fraPlot.setLayout(layout)
        self.good_pump_curve = False

        self.VOLCURVE = 0
        self.HEADCURVE = 1
        self.EFFCURVE = 2
        self.HLOSSCURVE = 3
        self.MAXPOINTS = 51
        self.TINY = 1.e-6
        self.Xlabels = {CurveType.VOLUME : " Height",
                       CurveType.PUMP : " Flow",
                       CurveType.EFFICIENCY : " Flow",
                       CurveType.HEADLOSS : " Flow",
                        CurveType.UNSET : ""}
        self.Ylabels = {CurveType.VOLUME : " Volume",
                       CurveType.PUMP : " Head",
                       CurveType.EFFICIENCY : " Efficiency",
                       CurveType.HEADLOSS : " Headloss",
                        CurveType.UNSET : ""}
        self.Xunits = {}
        self.Yunits = {}
        self.Xlabel = ""
        self.Ylabel = ""
        self.Xunit = ""
        self.Yunit = ""
        self.MSG_OUT_OF_ORDER = ' values are not in ascending order.'
        self.MSG_BAD_CURVE = 'Illegal pump curve. Continue editing?'
        self.FMT_EQN = ' Head = %f%-.4g(Flow)^%f'
        self.TXT_PERCENT = ' (%)'
        self.TXT_CUBIC = ' (cubic '
        self.TXT_PUMP = 'PUMP'
        self.TXT_BAD_CURVE = ' Illegal pump curve.'
        self.TXT_INVALID_CURVE = " Invalid pump curve."
        self.TXT_OPEN_CURVE_TITLE = 'Open a Curve'
        self.TXT_SAVE_CURVE_TITLE = 'Save Curve As'
        self.TXT_CURVE_FILTER = 'Curve files (*.CRV)|*.CRV|All files|*.*'
        self.TXT_CURVE_HEADER = 'EPANET Curve Data'

        self.X = np.arange(self.MAXPOINTS, dtype=float) * float('NaN')
        self.Y = np.arange(self.MAXPOINTS, dtype=float) * float('NaN')
        self.xvals = []
        self.yvals = []

        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first curve if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

        self.txtEquation.setEnabled(False) #only for display
        curve_type = core.epanet.curves.CurveType[self.cboCurveType.currentText()]
        if curve_type == CurveType.PUMP and not self.good_pump_curve:
            self.txtEquation.setText(self.TXT_BAD_CURVE)

        self.loaded = True

    def set_from(self, curve):
        if not isinstance(curve, Curve):
            curve = self.section.value[curve]
        if isinstance(curve, Curve):
            self.editing_item = curve
        self.txtCurveName.setText(str(curve.name))
        self.txtDescription.setText(str(curve.description))
        LengthUnits = "???"
        FlowUnits = "???"
        if self.project:
            FlowUnits = self.project.options.hydraulics.flow_units.name
        self.Xunits[CurveType.VOLUME] = ' (' + LengthUnits + ')'
        self.Xunits[CurveType.PUMP] = ' (' + FlowUnits + ')'
        self.Xunits[CurveType.EFFICIENCY] = self.Xunits[CurveType.PUMP]
        self.Xunits[CurveType.HEADLOSS] = self.Xunits[CurveType.PUMP]
        self.Xunits[CurveType.UNSET] = ""
        self.Yunits[CurveType.VOLUME] = self.TXT_CUBIC + LengthUnits + ')'
        self.Yunits[CurveType.PUMP] = ' (' + LengthUnits + ')'
        self.Yunits[CurveType.EFFICIENCY] = self.TXT_PERCENT
        self.Yunits[CurveType.HEADLOSS] = ' (' + LengthUnits + ')'
        self.Yunits[CurveType.UNSET] = ""
        ui.convenience.set_combo(self.cboCurveType, curve.curve_type)
        point_count = -1
        for point in curve.curve_xy:
            point_count += 1
            led = QtGui.QLineEdit(str(point[0]))
            self.tblMult.setItem(point_count, 0, QtGui.QTableWidgetItem(led.text()))
            led = QtGui.QLineEdit(str(point[1]))
            self.tblMult.setItem(point_count, 1, QtGui.QTableWidgetItem(led.text()))
        #CurveGrid.RowCount= MAXPOINTS + 1
        #CurveID.MaxLength= MAXID; // Max.chars. in a ID
        #ActiveControl= CurveID

    def GetData(self):
        n = 0
        for row in range(self.tblMult.rowCount()):
            if self.tblMult.item(row,0) and self.tblMult.item(row,1):
                x_val, x_val_good = ParseData.floatTryParse(self.tblMult.item(row, 0).text())
                y_val, y_val_good = ParseData.floatTryParse(self.tblMult.item(row, 1).text())
                if x_val_good and y_val_good:
                    if row + 1 >= self.MAXPOINTS:
                        break
                    else:
                        self.X[row + 1] = x_val
                        self.Y[row + 1] = y_val
                        n += 1
            else:
                return n
        return n

    def resetData(self):
        for i in range(0, len(self.X)):
            self.X[i] *= float('NaN')
            self.Y[i] *= float('NaN')
        self.txtEquation.setText("")

    def load_curve_data(self):
        directory = self._main_form.program_settings.value("DataDir", "")
        #file_name = QtGui.QFileDialog.getSaveFileName(self, "Save Curve", directory, "Curve files (*.crv)")
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Curve Data File", directory, "Curve Files (*.crv)")
        if os.path.exists(file_name):
            self._main_form.program_settings.setValue("DataDir", os.path.dirname(file_name))
            self._main_form.program_settings.sync()

        if file_name:
            with open(file_name, "r") as open_file:
                lines = open_file.readlines()

            if len(lines) > 1:
                ui.convenience.set_combo(self.cboCurveType, lines[1].strip())
            if len(lines) > 2:
                a = lines[2].split()
                self.txtCurveName.setText(a[len(a) - 1])
            if len(lines) > 3:
                curve_xy = []
                for i in range(3, len(lines)):
                    try:
                        x, y = lines[i].split()
                        xval, xval_is_good = ParseData.floatTryParse(x)
                        yval, yval_is_good = ParseData.floatTryParse(y)
                        if xval_is_good and yval_is_good:
                            curve_xy.append((x, y))

                        point_count = -1
                        for point in curve_xy:
                            point_count += 1
                            led = QtGui.QLineEdit(str(point[0]))
                            self.tblMult.setItem(point_count, 0, QtGui.QTableWidgetItem(led.text()))
                            led = QtGui.QLineEdit(str(point[1]))
                            self.tblMult.setItem(point_count, 1, QtGui.QTableWidgetItem(led.text()))

                        pass
                    except Exception as ex:
                        pass

    def save_curve_data(self):
        directory = self._main_form.program_settings.value("DataDir", "")
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save Curve", directory, "Curve files (*.crv)")
        if os.path.exists(file_name):
            self._main_form.program_settings.setValue("DataDir", os.path.dirname(file_name))
            self._main_form.program_settings.sync()
        if file_name:
            #self.add_recent_project(file_name)
            path_only, file_only = os.path.split(file_name)
            try:
                self.curve_data_to_file(file_name)
                self.setWindowTitle(self._main_form.model + " - " + file_only)
                if path_only != directory:
                    self._main_form.program_settings.setValue("DataDir", path_only)
                    self._main_form.program_settings.sync()
            except Exception as ex:
                print(str(ex) + '\n' + str(traceback.print_exc()))
                QMessageBox.information(self, self._main_form.model,
                                        "Error saving {0}\nin {1}\n{2}\n{2}".format(
                                            file_only, path_only,
                                            str(ex), str(traceback.print_exc())),
                                        QMessageBox.Ok)

            #self._main_form.undo_stack.setClean()

    def curve_data_to_file(self, file_name):
        if file_name:
            for i in range(0, len(self.X)):
                self.X[i] *= float('NaN')
                self.Y[i] *= float('NaN')
            N = self.GetData()
            with open(file_name, 'w') as writer:
                #writer.writelines(self.as_text(project))
                writer.write("EPANET Curve Data\n")
                writer.write(self.cboCurveType.currentText() + "\n")
                writer.write("PUMP: Pump Curve for Pump " + self.editing_item.name + "\n")
                for i in range(0, len(self.X)):
                    if np.isnan(self.X[i]) or np.isnan(self.Y[i]):
                        pass
                    else:
                        writer.write("%s  %s\n" % (str(self.X[i]), str(self.Y[i])))

    def tblMult_cellChanged(self, row, col):
        if col == 1:
            if self.tblMult.item(row, 0) and self.tblMult.item(row, 1):
                self.setupPlotData()

    def setupPlotData(self):
        self.resetData()
        N = self.GetData()
        if N < 1:
            return
        curve_type = core.epanet.curves.CurveType[self.cboCurveType.currentText()]
        if curve_type == CurveType.PUMP:
            # for PUMP curve, only plot 1- or 3-point pump head curves
            if N == 1 or N == 3:
                # Fit power function to 1- or 3-point pump head curves
                if self.FitPumpCurve(N):
                    self.good_pump_curve = True
                    self.display_curve()
                else:
                    # Invalid pump curve - retrieve curve points again
                    #self.txtEquation.setText(self.TXT_INVALID_CURVE)
                    self.good_pump_curve = False
                    self.display_curve()
                    N = self.GetData()
                    if len(self.txtEquation.text()) == 0:
                        self.txtEquation.setText(self.TXT_BAD_CURVE)
            else:
                self.good_pump_curve = False
                self.display_curve()
        else:
            # if not pump curve, then simply plot x, y in the data grid
            self.good_pump_curve = False
            self.display_curve()

    def display_curve(self):
        # plot curve
        #self.setParent(self._main_form)
        n = 0
        # honor the original FitPumpCurve's algorithm of setting array start at position 1
        #xvals = np.arange(n + 1, dtype=float) * float('NaN')
        #yvals = np.arange(n + 1, dtype=float) * float('NaN')
        del self.xvals[:]
        del self.yvals[:]
        sort_needed = False
        x_prev = float('-inf')
        for i in range(1, len(self.X)):
            if np.isnan(self.X[i]) or np.isnan(self.Y[i]):
                break
                pass
            else:
                if self.X[i] >= x_prev:
                    x_prev = self.X[i]
                else:
                    sort_needed = True
                self.xvals.append(self.X[i])
                self.yvals.append(self.Y[i])
                n += 1
        if n > 0:
            if sort_needed:
                self.sortData()
                pass
            self.plot.setData(self.xvals, self.yvals,
                              self.Xlabel + self.Xunit,
                              self.Ylabel + self.Yunit,
                              self.good_pump_curve)
        pass

    def sortData(self):
        if len(self.xvals) > 1 and len(self.yvals) > 1:
            d = {}
            for i in range(0, len(self.xvals)):
                d[self.xvals[i]] = i
            sd = sorted(d)
            del self.xvals[:]
            new_yvals = []
            for i in range(0, len(sd)):
                self.xvals.append(sd[i])
                new_yvals.append(self.yvals[d[sd[i]]])
            del self.yvals[:]
            for i in range (0, len(new_yvals)):
                self.yvals.append(new_yvals[i])
            del new_yvals

    def cmdOK_Clicked(self):
        if not self.loaded:
            return
        # TODO: Check for duplicate curve name
        # TODO: Check if X-values are in ascending order
        # TODO: Check for legal pump curve
        self.editing_item.name = self.txtCurveName.text()
        self.editing_item.description = self.txtDescription.text()
        self.editing_item.curve_type = core.epanet.curves.CurveType[self.cboCurveType.currentText()]
        self.editing_item.curve_xy = []
        for row in range(self.tblMult.rowCount()):
            if self.tblMult.item(row,0) and self.tblMult.item(row,1):
                x = self.tblMult.item(row, 0).text()
                y = self.tblMult.item(row, 1).text()
                if len(x) > 0 and len(y) > 0:
                    self.editing_item.curve_xy.append((x, y))
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
        else:
            pass
            # TODO: self._main_form.edited_?
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboCurveType_currentIndexChanged(self, newIndex):
        curve_type = core.epanet.curves.CurveType[self.cboCurveType.currentText()]
        # if curve_type == CurveType.PUMP:
        #     self.tblMult.setHorizontalHeaderLabels(("Flow", "Head"))
        # elif curve_type == CurveType.EFFICIENCY:
        #     self.tblMult.setHorizontalHeaderLabels(("Flow", "Efficiency"))
        # elif curve_type == CurveType.HEADLOSS:
        #     self.tblMult.setHorizontalHeaderLabels(("Flow", "Headloss"))
        # elif curve_type == CurveType.VOLUME:
        #     self.tblMult.setHorizontalHeaderLabels(("Height", "Volume"))
        self.Xlabel = self.Xlabels[curve_type]
        self.Ylabel = self.Ylabels[curve_type]
        self.Xunit = self.Xunits[curve_type]
        self.Yunit = self.Yunits[curve_type]
        self.tblMult.setHorizontalHeaderLabels((self.Xlabel, self.Ylabel))
        if curve_type == CurveType.PUMP:
            pass
        else:
            self.txtEquation.setText("")
            self.txtEquation.setEnabled(False)
        self.setupPlotData()

    def FitPumpCurve(self, N):
        # From Dcurve.pas, LR
        # Fits 1- or 3-point head curve data to power function
        # input N: Integer
        # return: Boolean
        h0 = 0.0
        h1 = 0.0
        h2 = 0.0
        h4 = 0.0
        h5 = 0.0
        q0 = 0.0
        q1 = 0.0
        q2 = 0.0
        a  = 0.0
        a1 = 0.0
        b  = 0.0
        c  = 0.0
        I = 0
        Iter = 0

        if N == 1:
            q0 = 0.0
            q1 = self.X[1]
            h1 = self.Y[1]
            h0 = 1.33334 * h1
            q2 = 2.0 * q1
            h2 = 0.0
        else:
            q0 = self.X[1]
            h0 = self.Y[1]
            q1 = self.X[2]
            h1 = self.Y[2]
            q2 = self.X[3]
            h2 = self.Y[3]

        a= h0
        b= 0.0
        c= 1.0

        if h0 < self.TINY \
        or (h0 - h1 < self.TINY) \
        or (h1 - h2 < self.TINY) \
        or (q1 - q0 < self.TINY) \
        or (q2 - q1 < self.TINY):
             Result = False
        else:
            a = h0
            Result = False
            for Iter in xrange(1, 6): # 1 to 5 do
                h4 = a - h1
                h5 = a - h2
                #c = ln(h5/h4)/ln(q2/q1)
                c = np.log(h5/h4) / np.log(q2/q1)
                '''
                ************************************************
                NOTE: If c < 1.0 then pump curve is convex which
                might cause convergence problems. This was
                permitted in Version 1.x so it is kept the
                same here. We might want to enforce c >= 1
                in the future.
                *************************************************
                '''
                if (c <= 0.0) or (c > 20.0):
                    break
                #b = -h4/Power(q1,c)
                b = -h4 / (q1 ** c)
                if b > 0.0:
                    break
                #a1 = h0 - b * Power(q0,c)
                a1 = h0 - b * (q0 ** c)
                if abs(a1 - a) < 0.01:
                    Result = True
                    break
                a = a1

        if Result:
            N = 25
            #with CurveGrid do
            #  if N > RowCount then N = RowCount
            if N > self.tblMult.rowCount():
                N = self.tblMult.rowCount()
            h4 = -a/b
            h5 = 1.0/c
            #q1 = Power(h4,h5)
            q1 = h4 ** h5
            q1 = q1/N
            self.X[1] = 0.0
            self.Y[1] = a
            for I in xrange(2, N + 1): #2 to N do:
                self.X[I] = (I-1)*q1
                #Y[I] = a + b*Power(X[I],c)
                self.Y[I] = a + b * (self.X[I] ** c)
            self.txtEquation.setEnabled(True)
            #CurveEqn.Caption = Format(FMT_EQN,[a,b,c])
            self.txtEquation.setText(self.FMT_EQN % (a, b, c))
        else:
            #CurveEqn.Caption = self.TXT_BAD_CURVE
            self.txtEquation.setText(self.TXT_BAD_CURVE)
            self.txtEquation.setEnabled(False)
        #EqnLabel.Enabled = True
        return Result

class CurvePlot(BasePlot):
    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        BasePlot.__init__(self, main_form, width, height, dpi)
        self.line, = self.axes.plot([],[], 'r-')
        pass

    def setData(self, X, Y, Xlabel, Ylabel, good_pump_curve):
        color = self.get_colors()
        #self.axes.scatter(self.X, self.Y, s=10, c=color, marker="o", label="")
        #self.axes.legend(loc='upper left')
        self.line.set_xdata(X)
        self.line.set_ydata(Y)
        if good_pump_curve:
            self.line.set_marker(None)
        else:
            self.line.set_marker("s")
            self.line.set_markeredgecolor("black")
            self.line.set_markerfacecolor("green")

        self.setXlabel(Xlabel)
        self.setYlabel(Ylabel)
        self.axes.relim()
        self.axes.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        #self.setTitle('Pump head curve for %s' % aData.name)
        pass

    def get_colors(self):
        return QColor("red")

