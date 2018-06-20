import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.swmm.options
from ui.SWMM.frmTimeStepsDesigner import Ui_frmTimeSteps
import math

class frmTimeSteps(QMainWindow, Ui_frmTimeSteps):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/simulationoptions_timesteps.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        section = project.options.time_steps
        self.cbxSkip.setChecked(section.skip_steady_state)
        self.sbxLateral.setValue(int(section.lateral_inflow_tolerance))
        self.sbxSystem.setValue(int(section.system_flow_tolerance))

        (days, hours, minutes, seconds) = frmTimeSteps.split_days(section.dry_step)
        self.sbxDry.setValue(days)
        self.tmeDry.setTime(QtCore.QTime(hours, minutes, seconds))

        (days, hours, minutes, seconds) = frmTimeSteps.split_days(section.wet_step)
        self.sbxWet.setValue(days)
        self.tmeWet.setTime(QtCore.QTime(hours, minutes, seconds))

        (days, hours, minutes, seconds) = frmTimeSteps.split_days(section.report_step)
        self.sbxReportDay.setValue(days)
        self.tmeReport.setTime(QtCore.QTime(hours, minutes, seconds))

        routing_time = QtCore.QTime(0, 0, 0).secsTo(QtCore.QTime.fromString(section.routing_step, section.TIME_FORMAT))
        self.txtRouting.setText(str(routing_time))

    @staticmethod
    def split_days(hms):
        """
        Args:
            hms: string containing two colons formatted as hours:minutes:seconds

        Returns:
            days, hours, minutes, and seconds as integers
        """
        (h, m, s) = hms.split(':')
        (hours, minutes, seconds) = (int(h), int(m), int(s))
        days = int(math.floor(hours / 24))
        hours -= days * 24
        return (days, hours, minutes, seconds)

    @staticmethod
    def controls_to_hms(sbx, tme):
        hours = tme.time().hour() + sbx.value() * 24
        (minutes, seconds) = (tme.time().minute(), tme.time().second())
        return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)


    def cmdOK_Clicked(self):
        section = self._main_form.project.options.time_steps
        section.skip_steady_state = self.cbxSkip.isChecked()
        section.lateral_inflow_tolerance = str(self.sbxLateral.value())
        section.system_flow_tolerance = str(self.sbxSystem.value())

        section.dry_step = frmTimeSteps.controls_to_hms(self.sbxDry, self.tmeDry)
        section.wet_step = frmTimeSteps.controls_to_hms(self.sbxWet, self.tmeWet)
        section.report_step = frmTimeSteps.controls_to_hms(self.sbxReportDay, self.tmeReport)
        routing_time = QtCore.QTime(0, 0, 0).addSecs(int(self.txtRouting.text()))
        section.routing_step = "{:02}:{:02}:{:02}".format(routing_time.hour(), routing_time.minute(), routing_time.second())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
