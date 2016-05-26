import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTimeSeriesPlotDesigner import Ui_frmTimeSeriesPlot
from ui.SWMM.frmTimeSeriesSelection import frmTimeSeriesSelection
from ui.help import HelpHandler


class frmTimeSeriesPlot(QtGui.QMainWindow, Ui_frmTimeSeriesPlot):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), self.btnAdd_Clicked)

        # self.set_from(parent.project)
        self._parent = parent


    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        if project and self.output:
            for time_index in range(0, self.output.numPeriods - 1):
                self.cboStart.addItem(str(time_index))  # self.report.get_time_string(time_index))
            # self.rbnNodes.setChecked(True)
            # self.rbnNodes_Clicked()

    def btnAdd_Clicked(self):
        self._frmTimeSeriesSelection = frmTimeSeriesSelection(self.parent())
        self._frmTimeSeriesSelection.show()

    def cmdOK_Clicked(self):
        # section = self._parent.project.find_section("CONTROLS")
        # section.set_text(str(self.txtControls.toPlainText()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
