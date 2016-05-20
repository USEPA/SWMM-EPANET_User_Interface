import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmStatisticsReportDesigner import Ui_frmStatisticsReport
from ui.help import HelpHandler


class frmStatisticsReport(QtGui.QMainWindow, Ui_frmStatisticsReport):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        # self.set_from(parent.project)
        self._parent = parent

    # def set_from(self, project):
        # section = core.epanet.project.Control()
        # section = project.find_section("CONTROLS")
        # self.txtControls.setPlainText(str(section.get_text()))

    def cmdCancel_Clicked(self):
        self.close()
