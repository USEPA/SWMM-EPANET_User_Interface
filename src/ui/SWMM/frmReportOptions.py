import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options.report
from ui.SWMM.frmReportOptionsDesigner import Ui_frmReportOptions


class frmReportOptions(QtGui.QMainWindow, Ui_frmReportOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.swmm.options.report.Report()
        section = project.find_section("REPORT")
        self.cbxContinuity.setChecked(section.continuity)
        self.cbxControls.setChecked(section.controls)
        self.cbxFlow.setChecked(section.flow_stats)
        self.cbxInput.setChecked(section.input)
        # add nodes to list 1
        # add links to list 2
        # add subcatchments to list 3

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("REPORT")
        section.continuity = self.cbxContinuity.isChecked()
        section.controls = self.cbxControls.isChecked()
        section.flow_stats = self.cbxFlow.isChecked()
        section.input = self.cbxInput.isChecked()
        # if none selected NONE, ALL, or list
        section.nodes = "NONE"
        section.links = "NONE"
        section.subcatchments = "NONE"
        self.close()

    def cmdCancel_Clicked(self):
        self.close()