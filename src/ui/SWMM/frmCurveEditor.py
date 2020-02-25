import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import *
from ui.help import HelpHandler
import core.swmm.curves
from ui.SWMM.frmCurveEditorDesigner import Ui_frmCurveEditor
import ui.convenience
from core.swmm.curves import CurveType
from core.swmm.curves import Curve
# from PyQt5.QtGui import *
from ui.model_utility import ParseData
import os
import traceback
import numpy as np
import pandas as pd
from ui.frmPlotViewer import frmPlotViewer


class frmCurveEditor(QMainWindow, Ui_frmCurveEditor):
    def __init__(self, main_form, title, curve_type, edit_these, new_item):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/curveeditordialog.htm"
        self.setupUi(self)
        if title:
            self.setWindowTitle(title)
        self.cboCurveType.clear()
        ui.convenience.set_combo_items(core.swmm.curves.CurveType, self.cboCurveType)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.btnSave.clicked.connect(self.save_curve_data)
        self.btnLoad.clicked.connect(self.load_curve_data)
        self.btnHelp.clicked.connect(self.show_help)
        self.btnView.clicked.connect(self.btnView_Clicked)
        # self.cboCurveType.clicked.connect(self.cboCurveType_currentIndexChanged)
        self.cboCurveType.currentIndexChanged.connect(self.cboCurveType_currentIndexChanged)
        # self.set_from(main_form.project)   # do after init to set curve type
        self._main_form = main_form
        self.curve_type = curve_type
        self.project = main_form.project
        self.section = self.project.curves
        self.X = []
        self.Y = []
        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first transect if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

    def set_from(self, curve):
        flow_units = self._main_form.project.options.flow_units.name
        if not isinstance(curve, Curve):
            curve = self.section.value[curve]
        if isinstance(curve, Curve):
            self.editing_item = curve
            self.tblMult.setRowCount(max(len(curve.curve_xy) + 1, self.tblMult.rowCount()))
        if self.curve_type == "CONTROL":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Controller Value","Control Setting"))
        elif self.curve_type == "DIVERSION":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Inflow (" + flow_units + ")", "Outflow (" + flow_units + ")"))
        elif self.curve_type == "PUMP":
            self.cboCurveType.setVisible(True)
            self.lblCurveType.setVisible(True)

            if curve.curve_type.name == "PUMP1":
                if self._main_form.project.metric:
                    self.tblMult.setHorizontalHeaderLabels(("Volume (m3)", "Flow (" + flow_units + ")"))
                else:
                    self.tblMult.setHorizontalHeaderLabels(("Volume (ft3)", "Flow (" + flow_units + ")"))
            if curve.curve_type.name == "PUMP2":
                if self._main_form.project.metric:
                    self.tblMult.setHorizontalHeaderLabels(("Depth (m)", "Flow (" + flow_units + ")"))
                else:
                    self.tblMult.setHorizontalHeaderLabels(("Depth (ft)", "Flow (" + flow_units + ")"))
            if curve.curve_type.name == "PUMP3":
                if self._main_form.project.metric:
                    self.tblMult.setHorizontalHeaderLabels(("Head (m)", "Flow (" + flow_units + ")"))
                else:
                    self.tblMult.setHorizontalHeaderLabels(("Head (ft)", "Flow (" + flow_units + ")"))
            if curve.curve_type.name == "PUMP4":
                if self._main_form.project.metric:
                    self.tblMult.setHorizontalHeaderLabels(("Depth (m)", "Flow (" + flow_units + ")"))
                else:
                    self.tblMult.setHorizontalHeaderLabels(("Depth (ft)", "Flow (" + flow_units + ")"))

            self.cboCurveType.clear()
            self.cboCurveType.addItems(("TYPE1","TYPE2","TYPE3","TYPE4"))
        elif self.curve_type == "RATING":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Head (m)", "Outflow (" + flow_units + ")"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Head (ft)", "Outflow (" + flow_units + ")"))
        elif self.curve_type == "SHAPE":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            self.tblMult.setHorizontalHeaderLabels(("Depth/Full Depth","Width/Full Depth"))
        elif self.curve_type == "STORAGE":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Depth (m)", "Area (m2)"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Depth (ft)", "Area (ft2)"))
        elif self.curve_type == "TIDAL":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Hour of Day", "Stage (m)"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Hour of Day", "Stage (ft)"))
        elif self.curve_type == "WEIR":
            self.cboCurveType.setVisible(False)
            self.lblCurveType.setVisible(False)
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Head (m)", "Coefficient"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Head (ft)", "Coefficient"))

        self.txtCurveName.setText(str(curve.name))
        self.txtDescription.setText(str(curve.comment))
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
             led = QLineEdit(str(point[0]))
             self.tblMult.setItem(point_count,0,QTableWidgetItem(led.text()))
             led = QLineEdit(str(point[1]))
             self.tblMult.setItem(point_count,1,QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        # TODO: Check for blank/duplicate curve name
        # TODO: Check if X-values are in ascending order
        orig_name = self.editing_item.name
        orig_comment = self.editing_item.comment
        orig_type = self.editing_item.curve_type
        orig_xy = self.editing_item.curve_xy

        self.editing_item.name = self.txtCurveName.text()
        self.editing_item.comment = self.txtDescription.text()
        if len(self.editing_item.comment) > 0:
            if self.editing_item.comment[0] != ';':
                self.editing_item.comment = ';' + self.editing_item.comment
        # curve.curve_type = core.swmm.curves.CurveType[self.cboCurveType.currentText()]
        if self.curve_type == "PUMP":
            if self.cboCurveType.currentIndex() == 0:
                self.editing_item.curve_type = core.swmm.curves.CurveType["PUMP1"]
            if self.cboCurveType.currentIndex() == 1:
                self.editing_item.curve_type = core.swmm.curves.CurveType["PUMP2"]
            if self.cboCurveType.currentIndex() == 2:
                self.editing_item.curve_type = core.swmm.curves.CurveType["PUMP3"]
            if self.cboCurveType.currentIndex() == 3:
                self.editing_item.curve_type = core.swmm.curves.CurveType["PUMP4"]
        self.editing_item.curve_xy = []
        for row in range(self.tblMult.rowCount()):
            if self.tblMult.item(row,0) and self.tblMult.item(row,1):
                x = self.tblMult.item(row,0).text()
                y = self.tblMult.item(row,1).text()
                if len(x) > 0 and len(y) > 0:
                    self.editing_item.curve_xy.append((x, y))
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
            self._main_form.mark_project_as_unsaved()
        else:
            pass
            # TODO: self._main_form.edited_?

        if orig_name != self.editing_item.name or \
            orig_comment != self.editing_item.comment or \
            orig_type != self.editing_item.curve_type or \
            orig_xy != self.editing_item.curve_xy:
            self._main_form.mark_project_as_unsaved()

        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboCurveType_currentIndexChanged(self, newIndex):
        curve_type = self.cboCurveType.currentText()
        flow_units = self._main_form.project.options.flow_units.name
        if curve_type == "TYPE1":
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Volume (m3)", "Flow (" + flow_units + ")"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Volume (ft3)", "Flow (" + flow_units + ")"))
        elif curve_type == "TYPE2":
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Depth (m)", "Flow (" + flow_units + ")"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Depth (ft)", "Flow (" + flow_units + ")"))
        elif curve_type == "TYPE3":
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Head (m)", "Flow (" + flow_units + ")"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Head (ft)", "Flow (" + flow_units + ")"))
        elif curve_type == "TYPE4":
            if self._main_form.project.metric:
                self.tblMult.setHorizontalHeaderLabels(("Depth (m)", "Flow (" + flow_units + ")"))
            else:
                self.tblMult.setHorizontalHeaderLabels(("Depth (ft)", "Flow (" + flow_units + ")"))

    def load_curve_data(self):
        directory = self._main_form.program_settings.value("DataDir", "")
        file_name, ftype = QFileDialog.getOpenFileName(self, "Open Curve Data File", directory, "Curve Files (*.dat)")
        if os.path.exists(file_name):
            self._main_form.program_settings.setValue("DataDir", os.path.dirname(file_name))
            self._main_form.program_settings.sync()

        if file_name:
            with open(file_name, "r") as open_file:
                lines = open_file.readlines()

            if len(lines) > 1:
                a = lines[1].split()
                self.txtDescription.setText(a[len(a) - 1])
            if len(lines) > 2:
                curve_xy = []
                for i in range(2, len(lines)):
                    try:
                        x, y = lines[i].split()
                        xval, xval_is_good = ParseData.floatTryParse(x)
                        yval, yval_is_good = ParseData.floatTryParse(y)
                        if xval_is_good and yval_is_good:
                            curve_xy.append((x, y))

                        point_count = -1
                        for point in curve_xy:
                            point_count += 1
                            led = QLineEdit(str(point[0]))
                            self.tblMult.setItem(point_count, 0, QTableWidgetItem(led.text()))
                            led = QLineEdit(str(point[1]))
                            self.tblMult.setItem(point_count, 1, QTableWidgetItem(led.text()))

                        pass
                    except Exception as ex:
                        pass

    def save_curve_data(self):
        directory = self._main_form.program_settings.value("DataDir", "")
        file_name, ftype = QFileDialog.getSaveFileName(self, "Save Curve Data File", directory, "Curve files (*.dat)")
        if os.path.exists(file_name):
            self._main_form.program_settings.setValue("DataDir", os.path.dirname(file_name))
            self._main_form.program_settings.sync()
        if file_name:
            path_only, file_only = os.path.split(file_name)
            try:
                self.curve_data_to_file(file_name)
            except Exception as ex:
                print(str(ex) + '\n' + str(traceback.print_exc()))
                QMessageBox.information(self, self._main_form.model,
                                        "Error saving {0}\nin {1}\n{2}\n{2}".format(
                                            file_only, path_only,
                                            str(ex), str(traceback.print_exc())),
                                        QMessageBox.Ok)

    def curve_data_to_file(self, file_name):
        if file_name:
            with open(file_name, 'w') as writer:
                #writer.writelines(self.as_text(project))
                writer.write("EPASWMM Curve Data\n")
                writer.write(self.txtDescription.text() + "\n")
                for row in range(self.tblMult.rowCount()):
                    if self.tblMult.item(row, 0) and self.tblMult.item(row, 1):
                        x = self.tblMult.item(row, 0).text()
                        y = self.tblMult.item(row, 1).text()
                        if len(x) > 0 and len(y) > 0:
                            writer.write("%s  %s\n" % (str(x), str(y)))

    def show_help(self):
        self.helper.show_help()

    def GetData(self):
        # construct pandas time series from grid data
        del self.X[:]
        del self.Y[:]
        n = 0
        for row in range(self.tblMult.rowCount()):
            if self.tblMult.item(row,1):
                y_val, y_val_good = ParseData.floatTryParse(self.tblMult.item(row, 1).text())
                x_val, x_val_good = ParseData.floatTryParse(self.tblMult.item(row, 0).text())
                if y_val_good and x_val_good:
                    # as long as the values are good
                    self.Y.append(y_val)
                    self.X.append(x_val)
                    n += 1
            else:
                return n
        return n

    def btnView_Clicked(self):
        """
        Display the grid data with pandas dataframe plot function
        Returns: None
        """
        n = self.GetData()
        if n > 0:
            ds = pd.Series(self.Y, index=self.X)
            df = pd.DataFrame({'DS-':ds})
            # if Pump Type1 or Type2, plot as step function
            if self.curve_type == 'PUMP' and self.cboCurveType.currentIndex() in (0, 1):
                frm_plt = frmPlotViewer(df, 'step', self.curve_type + ' Curve ' + self.txtCurveName.text(),
                                        self.windowIcon(), self.tblMult.horizontalHeaderItem(0).text(),
                                        self.tblMult.horizontalHeaderItem(1).text())
            else:
                frm_plt = frmPlotViewer(df, 'xy', self.curve_type + ' Curve ' + self.txtCurveName.text(),
                                        self.windowIcon(), self.tblMult.horizontalHeaderItem(0).text(),
                                        self.tblMult.horizontalHeaderItem(1).text())
            frm_plt.setWindowTitle('Curve Viewer')
            frm_plt.setWindowModality(QtCore.Qt.ApplicationModal)
            frm_plt.show()
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.tblMult.currentRow() + 1 == self.tblMult.rowCount():
                self.tblMult.insertRow(self.tblMult.rowCount())