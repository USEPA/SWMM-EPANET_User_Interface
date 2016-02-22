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
        section = project.options.time_steps
        self.cbxSkip.setChecked(section.skip_steady_state)
        self.sbxLateral.setValue(section.lat_flow_tol)
        self.sbxSystem.setValue(section.sys_flow_tol)
        #self.sbxDry.setValue(section.dry_step)
        self.tmeDry.setTime(QtCore.QTime.fromString(section.dry_step, section.TIME_FORMAT))
        #self.sbxWet.setValue(section.wet_step)
        self.tmeWet.setTime(QtCore.QTime.fromString(section.wet_step, section.TIME_FORMAT))
        #self.sbxReportDay.setValue(QtCore.QTime.fromString(section.report_step, section.TIME_FORMAT))
        self.txtRouting.text = section.routing_step

    def cmdOK_Clicked(self):
        section = self._parent.project.options.time_steps
        section.skip_steady_state = self.cbxSkip.isChecked()
        section.lat_flow_tol = self.sbxLateral.value()
        section.sys_flow_tol = self.sbxSystem.value()
        #section.dry_step = self.sbxDry + self.tmeDry
        #section.wet_step = self.sbxWet + self.tmeWet
        #section.report_step = self.sbxReportDay + self.tmeReport
        section.routing_step = self.txtRouting.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()