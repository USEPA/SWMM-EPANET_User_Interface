import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTimeseriesDesigner import Ui_frmTimeseries


class frmTimeseries(QtGui.QMainWindow, Ui_frmTimeseries):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnFile, QtCore.SIGNAL("clicked()"), self.btnFile_Clicked)
        # QtCore.QObject.connect(self.btnView, QtCore.SIGNAL("clicked()"), self.btnView_Clicked)
        self._parent = parent
        self.timeseries_id = ''
        # set for first timeseries for now
        self.set_from(parent.project,'TS1')

    def set_from(self, project, timeseries_id):
        # section = core.swmm.project.SnowPack
        section = project.find_section("TIMESERIES")
        timeseries_list = section.value[0:]
        # assume we want to edit the first one
        self.timeseries_id = timeseries_id
        for timeseries in timeseries_list:
            if timeseries.name: # == timeseries_id
                # this is the timeseries we want to edit
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
        section = self._parent.project.find_section("TIMESERIES")
        timeseries_list = section.value[0:]
        for timeseries in timeseries_list:
            if timeseries.name == self.timeseries_id:
                # this is the timeseries
                timeseries.name = self.txtTimeseriesName.text()
                timeseries.comment = self.txtDescription.text()
                if self.rbnExternal.isChecked():
                    timeseries.file = self.txtExternalFile.text()
                    timeseries.dates = []
                    timeseries.times = []
                    timeseries.values = []
                else:
                    timeseries.dates = []
                    timeseries.times = []
                    timeseries.values = []
                    for row in range(self.tblTime.rowCount()):
                        if self.tblTime.item(row,2):
                            x = self.tblTime.item(row,2).text()
                            if len(x) > 0:
                                timeseries.dates.append(self.tblTime.item(row,0).text())
                                timeseries.times.append(self.tblTime.item(row,1).text())
                                timeseries.values.append(x)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def btnFile_Clicked(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open a Time Series", '',
                                                      "Time series files (*.DAT);;All files (*.*)")
        if file_name:
            self.txtExternalFile.setText(file_name)

    # def btnFile_Clicked(self):
