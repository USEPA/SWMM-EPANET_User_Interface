import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options
from ui.SWMM.frmTimeStepsDesigner import Ui_frmTimeSteps


class frmTimeSteps(QtGui.QMainWindow, Ui_frmTimeSteps):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.swmm.options.timesteps
        section = project.find_section("OPTIONS")
        self.cbxSkip.setChecked(section.TimeSteps.skip_steady_state)
        self.sbxLateral.setvalue(section.TimeSteps.lat_flow_tol)
        self.sbxSystem.setvalue(section.TimeSteps.sys_flow_tol)
        self.sbxDry.setvalue(section.TimeSteps.dry_step)
        self.tmeDry.setTime(section.TimeSteps.dry_step)
        self.sbxWet.setvalue(section.TimeSteps.wet_step)
        self.tmeWet.setTime(section.TimeSteps.wet_step)
        self.sbxReportDay.setvalue(section.TimeSteps.report_step)
        self.tmeReport.setTime(section.TimeSteps.report_step)
        self.txtRouting.text(section.TimeSteps.routing_step)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("OPTIONS")
        section.TimeSteps.skip_steady_state = self.cbxSkip
        section.TimeSteps.lat_flow_tol = self.sbxLateral
        section.TimeSteps.sys_flow_tol = self.sbxSystem
        section.TimeSteps.dry_step = self.sbxDry + self.tmeDry
        section.TimeSteps.wet_step = self.sbxWet + self.tmeWet
        section.TimeSteps.report_step = self.sbxReportDay + self.tmeReport
        section.TimeSteps.routing_step = self.txtRouting.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()