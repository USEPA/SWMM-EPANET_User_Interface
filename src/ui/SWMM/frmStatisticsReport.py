import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmStatisticsReportDesigner import Ui_frmStatisticsReport
from ui.help import HelpHandler


class frmStatisticsReport(QtGui.QMainWindow, Ui_frmStatisticsReport):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        # self.set_from(parent.project)
        self._main_form = main_form

    def set_from(self, project, output, object_name, object_id, variable_name, event_name, stat_name,
                 threshold_value, event_volume, separation_time):
        self.project = project
        self.output = output

        self.object_name = object_name      # Subcatchment
        self.object_id = object_id          # 1
        self.variable_name = variable_name  # Precipitation
        self.event_name = event_name        # Daily
        self.stat_name = stat_name          # Mean
        self.threshold_value = threshold_value   # 0
        self.event_volume = event_volume         # 0
        self.separation_time = separation_time   # 6

    def cmdCancel_Clicked(self):
        self.close()
