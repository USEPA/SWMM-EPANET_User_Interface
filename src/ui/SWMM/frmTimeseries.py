import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import *
from ui.SWMM.frmTimeseriesDesigner import Ui_frmTimeseries
from ui.help import HelpHandler
from core.swmm.timeseries import TimeSeries
from ui.model_utility import ParseData
import pandas as pd
#import matplotlib.pyplot as plt
from ui.frmPlotViewer import frmPlotViewer


class frmTimeseries(QMainWindow, Ui_frmTimeseries):
    def __init__(self, main_form, edit_these=[], new_item=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/timeserieseditordialog.htm"
        self.helper = HelpHandler(self)
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.btnFile.clicked.connect(self.btnFile_Clicked)
        self.btnView.clicked.connect(self.btnView_Clicked)
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.timeseries
        self.new_item = new_item
        self.hour_only = True
        self.X = []
        self.Y = []
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first timeseries if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

        if (main_form.program_settings.value("Geometry/" + "frmTimeseries_geometry") and
                main_form.program_settings.value("Geometry/" + "frmTimeseries_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmTimeseries_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmTimeseries_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, timeseries):
        if not isinstance(timeseries, TimeSeries):
            timeseries = self.section.value[timeseries]
        if isinstance(timeseries, TimeSeries):
            self.editing_item = timeseries
            self.txtTimeseriesName.setText(timeseries.name)
            self.txtDescription.setText(timeseries.comment)
            self.tblTime.setRowCount(max(len(timeseries.values) + 1, self.tblTime.rowCount()))
            if timeseries.file:
                if len(timeseries.file) > 0:
                    self.rbnExternal.setChecked(True)
                    self.txtExternalFile.setText(timeseries.file)
                else:
                    self.rbnTable.setChecked(True)
            else:
                self.rbnTable.setChecked(True)
            if self.rbnTable.isChecked():
                point_count = -1
                for value in timeseries.values:
                    point_count += 1
                    led = QLineEdit(str(timeseries.dates[point_count]))
                    self.tblTime.setItem(point_count,0,QTableWidgetItem(led.text()))
                    led = QLineEdit(str(timeseries.times[point_count]))
                    self.tblTime.setItem(point_count,1,QTableWidgetItem(led.text()))
                    led = QLineEdit(str(value))
                    self.tblTime.setItem(point_count,2,QTableWidgetItem(led.text()))

    def GetData(self):
        """
        construct pandas time series from grid data
        Returns:
        """
        del self.X[:] #datetime
        del self.Y[:] #value
        self.hour_only = True
        if self.tblTime.item(0, 0):
            if self.tblTime.item(0, 0).text():
                self.hour_only = False
        n = 0
        ldate = ""
        ltime = ""
        for row in range(self.tblTime.rowCount()):
            if self.tblTime.item(row,2):
                y_val, y_val_good = ParseData.floatTryParse(self.tblTime.item(row, 2).text())
                if y_val_good:
                    # as long as the value is good, then start parsing time stamp
                    self.Y.append(y_val)
                    if self.tblTime.item(row, 0):
                        if self.tblTime.item(row, 0).text():
                            ldate = self.tblTime.item(row, 0).text()
                    if self.tblTime.item(row, 1):
                        if self.tblTime.item(row, 1).text():
                            ltime = self.tblTime.item(row, 1).text()
                        else:
                            continue
                    if self.hour_only:
                        if ":" in ltime:
                            arr = ltime.split(":")
                            hr = 0
                            mm = 0
                            ss = 0
                            if len(arr) > 0:
                                hr = int(arr[0])
                            if len(arr) > 1:
                                mm = int(arr[1])
                            if len(arr) > 2:
                                ss = int(arr[2])
                            stamp = hr + mm / 60.0 + ss / 3600.0
                        else:
                            # if not in H:M format, then it is just fraction hours from beginning
                            stamp = float(ltime)
                    else:
                        stamp = pd.Timestamp(ldate + " " + ltime)

                    self.X.append(stamp)
                    n += 1
            else:
                return n
        return n

    def cmdOK_Clicked(self):

        orig_name = self.editing_item.name
        orig_comment = self.editing_item.comment
        orig_dates = self.editing_item.dates
        orig_times = self.editing_item.times
        orig_values = self.editing_item.values

        self.editing_item.name = self.txtTimeseriesName.text()
        self.editing_item.comment = self.txtDescription.text()
        if self.editing_item.comment and self.editing_item.comment[0] != ';':
            # Make sure comment starts with a semicolon
            self.editing_item.comment = '; ' + self.editing_item.comment
        if self.rbnExternal.isChecked():
            self.editing_item.file = self.txtExternalFile.text()
            self.editing_item.dates = []
            self.editing_item.times = []
            self.editing_item.values = []
        else:
            self.editing_item.dates = []
            self.editing_item.times = []
            self.editing_item.values = []
            for row in range(self.tblTime.rowCount()):
                try:
                    if self.tblTime.item(row, 2):
                        value_text = self.tblTime.item(row, 2).text()
                        if value_text:
                            item = self.tblTime.item(row, 0)
                            if item:
                                date_text = item.text()
                            else:
                                date_text = ''
                            item = self.tblTime.item(row, 1)
                            if item:
                                time_text = item.text()
                            else:
                                time_text = ''
                            self.editing_item.dates.append(date_text)
                            self.editing_item.times.append(time_text)
                            self.editing_item.values.append(value_text)
                except Exception as ex:
                    print("Skipping row " + str(row) + " of time series grid: " + str(ex))
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
            self._main_form.mark_project_as_unsaved()
        else:
            if orig_name != self.editing_item.name or \
                orig_comment != self.editing_item.comment or \
                orig_dates != self.editing_item.dates or \
                orig_times != self.editing_item.times or \
                orig_values != self.editing_item.values:
                self._main_form.mark_project_as_unsaved()
            pass
            # TODO: self._main_form.edited_?

        self._main_form.program_settings.setValue("Geometry/" + "frmTimeseries_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmTimeseries_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmTimeseries_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmTimeseries_state", self.saveState())
        self.close()

    def btnFile_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Open a Time Series", '',
                                                      "Time series files (*.DAT);;All files (*.*)")
        if file_name:
            self.txtExternalFile.setText('"' + file_name + '"')

    def btnView_Clicked(self):
        """
        Display the grid data with pandas dataframe plot function
        Returns: None
        """
        n = self.GetData()
        if n > 0:
            ts = pd.Series(self.Y, index=self.X)
            #plt.figure()
            #ts.plot()
            df = pd.DataFrame({'TS-' + self.txtTimeseriesName.text():ts})
            df.hour_only = self.hour_only
            frm_plt = frmPlotViewer(df,'time','Time Series ' + self.editing_item.name, self.windowIcon(), '', '')
            frm_plt.setWindowModality(QtCore.Qt.ApplicationModal)
            frm_plt.show()
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.tblTime.currentRow() + 1 == self.tblTime.rowCount():
                self.tblTime.insertRow(self.tblTime.rowCount())