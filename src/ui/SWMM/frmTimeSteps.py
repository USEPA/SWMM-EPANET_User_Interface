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
        self.sbxDry.setValue(project.options.dates.dry_days)

        section = project.options.time_steps
        self.cbxSkip.setChecked(section.skip_steady_state)
        self.sbxLateral.setValue(section.lat_flow_tol)
        self.sbxSystem.setValue(section.sys_flow_tol)

        self.tmeDry.setTime(QtCore.QTime.fromString(section.dry_step, section.TIME_FORMAT))
        self.tmeWet.setTime(QtCore.QTime.fromString(section.wet_step, section.TIME_FORMAT))
        self.tmeReport.setTime(QtCore.QTime.fromString(section.report_step, section.TIME_FORMAT))
        self.tmeRouting.setTime(QtCore.QTime.fromString(section.routing_step, section.TIME_FORMAT))

    def cmdOK_Clicked(self):
        self._project.options.dates.dry_days = self.sbxDry.value()
        section = self._parent.project.options.time_steps
        section.skip_steady_state = self.cbxSkip.isChecked()
        section.lat_flow_tol = self.sbxLateral.value()
        section.sys_flow_tol = self.sbxSystem.value()
        section.dry_step = format(self.tmeDry.time(), section.TIME_FORMAT)
        section.wet_step = format(self.tmeWet.time(), section.TIME_FORMAT)
        section.report_step = format(self.tmeReport.time(), section.TIME_FORMAT)
        section.routing_step = format(self.tmeRouting.time(), section.TIME_FORMAT)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()