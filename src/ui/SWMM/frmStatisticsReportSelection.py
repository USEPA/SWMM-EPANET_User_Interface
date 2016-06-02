import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmStatisticsReportSelectionDesigner import Ui_frmStatisticsReportSelection
from ui.SWMM.frmStatisticsReport import frmStatisticsReport
from ui.help import HelpHandler


class frmStatisticsReportSelection(QtGui.QMainWindow, Ui_frmStatisticsReportSelection):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        # self.set_from(parent.project)
        self._main_form = main_form

    # def set_from(self, project):
        # section = core.epanet.project.Control()
        # section = project.find_section("CONTROLS")
        # self.txtControls.setPlainText(str(section.get_text()))

    def cmdOK_Clicked(self):
        self._frmStatisticsReport = frmStatisticsReport(self._main_form)
        self._frmStatisticsReport.show()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
