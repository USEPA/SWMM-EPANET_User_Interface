import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmTimeseriesDesigner import Ui_frmTimeseries
from core.swmm.timeseries import TimeSeries


class frmTimeseries(QtGui.QMainWindow, Ui_frmTimeseries):
    def __init__(self, main_form, edit_these, new_item):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/timeserieseditordialog.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnFile, QtCore.SIGNAL("clicked()"), self.btnFile_Clicked)
        # QtCore.QObject.connect(self.btnView, QtCore.SIGNAL("clicked()"), self.btnView_Clicked)
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.timeseries
        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first timeseries if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

    def set_from(self, timeseries):
        if not isinstance(timeseries, TimeSeries):
            timeseries = self.section.value[timeseries]
        if isinstance(timeseries, TimeSeries):
            self.editing_item = timeseries
            self.txtTimeseriesName.setText(timeseries.name)
            self.txtDescription.setText(timeseries.comment)
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
                    led = QtGui.QLineEdit(str(timeseries.dates[point_count]))
                    self.tblTime.setItem(point_count,0,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(str(timeseries.times[point_count]))
                    self.tblTime.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(str(value))
                    self.tblTime.setItem(point_count,2,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
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
        else:
            pass
            # TODO: self._main_form.edited_?
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def btnFile_Clicked(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open a Time Series", '',
                                                      "Time series files (*.DAT);;All files (*.*)")
        if file_name:
            self.txtExternalFile.setText(file_name)

