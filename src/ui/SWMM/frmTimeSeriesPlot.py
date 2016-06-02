import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTimeSeriesPlotDesigner import Ui_frmTimeSeriesPlot
from ui.SWMM.frmTimeSeriesSelection import frmTimeSeriesSelection
from ui.help import HelpHandler


class frmTimeSeriesPlot(QtGui.QMainWindow, Ui_frmTimeSeriesPlot):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), self.btnAdd_Clicked)

        self._main_form = main_form


    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        if project and self.output:
            for time_index in range(0, self.output.numPeriods - 1):
                time_string = self.output.get_time_string(time_index)
                self.cboStart.addItem(time_string)
                self.cboEnd.addItem(time_string)
            self.cboStart.currentIndex = 0
            self.cboEnd.currentIndex = self.cboEnd.count() - 1
            # self.rbnNodes.setChecked(True)
            # self.rbnNodes_Clicked()
            # values = self.output.get_NodeSeries(0, 0)
            # for val in values:
            #     print '{:7.2f}'.format(val)

    def add(self, object_type, object_id, variable, legend, rightaxis):
        self.lstData.addItem(object_type + ' ' + object_id + ' ' + variable + ' ' + legend + ' ' + rightaxis)

    def btnAdd_Clicked(self):
        self._frmTimeSeriesSelection = frmTimeSeriesSelection(self._main_form)
        self._frmTimeSeriesSelection.set_from(self.project, self.output, self.add)
        self._frmTimeSeriesSelection.show()

    def cmdOK_Clicked(self):
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
