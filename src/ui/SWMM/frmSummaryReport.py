import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmSummaryReportDesigner import Ui_frmSummaryReport


class frmSummaryReport(QtGui.QMainWindow, Ui_frmSummaryReport):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._main_form = main_form

    # def set_from(self, project, control_type):
        # section = core.epanet.project.Control()

    def cmdCancel_Clicked(self):
        self.close()
