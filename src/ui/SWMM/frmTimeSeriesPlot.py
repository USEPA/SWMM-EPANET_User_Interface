import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import matplotlib.pyplot as plt
import core.swmm.project
from ui.SWMM.frmTimeSeriesPlotDesigner import Ui_frmTimeSeriesPlot
from ui.SWMM.frmTimeSeriesSelection import frmTimeSeriesSelection
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO


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

    def add(self, object_type, object_id, variable, axis, legend):
        item = object_type + ' ' + object_id + ' ' + variable + ' ' + axis + ' "' + legend + '"'
        self.lstData.addItem(item)

    def btnAdd_Clicked(self):
        self._frmTimeSeriesSelection = frmTimeSeriesSelection(self._main_form)
        self._frmTimeSeriesSelection.set_from(self.project, self.output, self.add)
        self._frmTimeSeriesSelection.show()

    def cmdOK_Clicked(self):
        self.plot_time()

    def cmdCancel_Clicked(self):
        self.close()

    def plot_time(self):
        fig = plt.figure()
        title = "Time Series Plot"
        fig.canvas.set_window_title(title)
        plt.title(title)
        x_values = []
        for time_index in range(0, self.output.numPeriods):
            x_values.append(self.output.elapsed_hours_at_index(time_index))

        for line in [str(self.lstData.item(i).text()) for i in range(self.lstData.count())]:
            object_type, object_id, variable, axis, legend_text = line.split(None, 4)
            legend_text = legend_text.strip('"')
            if object_type == "Node":
                item_index = self.output.get_NodeIndex(object_id)
                attribute_index = SMO.SMO_nodeAttributes[SMO.SMO_nodeAttributeNames.index(variable)]
                units = SMO.SMO_nodeAttributeUnits[attribute_index]
                y_values = self.output.get_NodeSeries(item_index, attribute_index)
            elif object_type == "Link":
                function = self.output.get_LinkSeries
                item_index = self.output.get_LinkIndex(object_id)
                attribute_index = SMO.SMO_linkAttributes[SMO.SMO_linkAttributeNames.index(variable)]
                units = SMO.SMO_linkAttributeUnits[attribute_index]
                y_values = self.output.get_LinkSeries(item_index, attribute_index)

            if y_values:
                plt.plot(x_values, y_values, label=legend_text)

        # fig.suptitle("Time Series Plot")
        # plt.ylabel(parameter_label)
        plt.xlabel("Time (hours)")
        plt.grid(True)
        plt.legend()
        plt.show()
