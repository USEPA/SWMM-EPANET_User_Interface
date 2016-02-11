import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.times
from core.epanet.options.times import StatisticOptions
from enum import Enum
from ui.EPANET.frmTimesOptionsDesigner import Ui_frmTimesOptions


class frmTimesOptions(QtGui.QMainWindow, Ui_frmTimesOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # TODO: function that populates combo box from Enum
        self.cboStatistic.addItems(("NONE", "AVERAGED", "MINIMUM", "MAXIMUM", "RANGE"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    @staticmethod
    def set_combo(combo_box, value):
        try:
            if isinstance(value, Enum):
                value = value.name
            index = combo_box.findText(value, QtCore.Qt.MatchFixedString)
            if index >= 0:
                combo_box.setCurrentIndex(index)
        except Exception as e:
            print(str(e))

    def set_from(self, project):
        # section = core.epanet.options.times.TimesOptions()
        section = project.find_section("TIMES")
        self.txtTotalDuration.setText(str(section.duration))
        self.txtHydraulic.setText(str(section.hydraulic_timestep))
        self.txtQuality.setText(str(section.quality_timestep))
        self.txtRule.setText(str(section.rule_timestep))
        self.txtPattern.setText(str(section.pattern_timestep))
        self.txtPatternTime.setText(str(section.pattern_start))
        self.txtReporting.setText(str(section.report_timestep))
        self.txtReportingTime.setText(str(section.report_start))
        self.txtClockStart.setText(str(section.start_clocktime))
        frmTimesOptions.set_combo(self.cboStatistic, section.statistic)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("TIMES")
        section.duration = self.txtTotalDuration.text()
        section.hydraulic_timestep = self.txtHydraulic.text()
        section.quality_timestep = self.txtQuality.text()
        section.rule_timestep = self.txtRule.text()
        section.pattern_timestep = self.txtPattern.text()
        section.pattern_start = self.txtPatternTime.text()
        section.report_timestep = self.txtReporting.text()
        section.report_start = self.txtReportingTime.text()
        section.start_clocktime = self.txtClockStart.text()
        section.statistic = core.epanet.options.times.StatisticOptions[self.cboStatistic.currentText()]
        self.close()

    def cmdCancel_Clicked(self):
        self.close()