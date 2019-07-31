import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.epanet.options.times
from core.epanet.options.times import StatisticOptions
from enum import Enum
from ui.EPANET.frmTimesOptionsDesigner import Ui_frmTimesOptions
import ui.convenience

class frmTimesOptions(QMainWindow, Ui_frmTimesOptions):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Anal0034.htm"
        self.setupUi(self)
        self.cboStatistic.clear()
        ui.convenience.set_combo_items(StatisticOptions, self.cboStatistic)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        # section = core.epanet.options.times.TimesOptions()
        section = project.times
        self.txtTotalDuration.setText(str(section.duration))
        self.txtHydraulic.setText(str(section.hydraulic_timestep))
        self.txtQuality.setText(str(section.quality_timestep))
        self.txtRule.setText(str(section.rule_timestep))
        self.txtPattern.setText(str(section.pattern_timestep))
        self.txtPatternTime.setText(str(section.pattern_start))
        self.txtReporting.setText(str(section.report_timestep))
        self.txtReportingTime.setText(str(section.report_start))
        self.txtClockStart.setText(str(section.start_clocktime))
        ui.convenience.set_combo(self.cboStatistic, section.statistic)

    def cmdOK_Clicked(self):
        section = self._main_form.project.times
        if section.duration != self.txtTotalDuration.text() or \
            section.hydraulic_timestep != self.txtHydraulic.text() or \
            section.quality_timestep != self.txtQuality.text() or \
            section.rule_timestep != self.txtRule.text() or \
            section.pattern_timestep != self.txtPattern.text() or \
            section.pattern_start != self.txtPatternTime.text() or \
            section.report_timestep != self.txtReporting.text() or \
            section.report_start != self.txtReportingTime.text() or \
            section.start_clocktime != self.txtClockStart.text() or \
            section.statistic != StatisticOptions[self.cboStatistic.currentText()]:
            self._main_form.mark_project_as_unsaved()

        section.duration = self.txtTotalDuration.text()
        section.hydraulic_timestep = self.txtHydraulic.text()
        section.quality_timestep = self.txtQuality.text()
        section.rule_timestep = self.txtRule.text()
        section.pattern_timestep = self.txtPattern.text()
        section.pattern_start = self.txtPatternTime.text()
        section.report_timestep = self.txtReporting.text()
        section.report_start = self.txtReportingTime.text()
        section.start_clocktime = self.txtClockStart.text()
        section.statistic = StatisticOptions[self.cboStatistic.currentText()]
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
