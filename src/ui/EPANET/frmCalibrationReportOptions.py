import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
import core.epanet.project
from ui.EPANET.frmCalibrationReportOptionsDesigner import Ui_frmCalibrationReportOptions
from ui.EPANET.frmCalibrationReport import frmCalibrationReport


class frmCalibrationReportOptions(QtGui.QMainWindow, Ui_frmCalibrationReportOptions):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Crea0079.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._main_form = main_form

    # def set_from(self, project, control_type):
        # section = core.epanet.project.Control()

    def cmdOK_Clicked(self):
        self._frmCalibrationReport = frmCalibrationReport(self._main_form)
        self._frmCalibrationReport.show()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
