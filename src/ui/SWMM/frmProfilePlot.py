import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmProfilePlotDesigner import Ui_frmProfilePlot
from ui.help import HelpHandler


class frmProfilePlot(QtGui.QMainWindow, Ui_frmProfilePlot):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        # self.help_topic = "swmm/src/src/controlrules.htm"
        self._main_form = main_form
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

    def set_from(self, project, output):
        self.project = project
        self.output = output

    def cmdOK_Clicked(self):
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
