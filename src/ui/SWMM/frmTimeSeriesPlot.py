import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import matplotlib.pyplot as plt
import colorsys
import numpy as np
import core.swmm.project
from ui.SWMM.frmTimeSeriesPlotDesigner import Ui_frmTimeSeriesPlot
from ui.SWMM.frmTimeSeriesSelection import frmTimeSeriesSelection
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO


class frmTimeSeriesPlot(QtGui.QMainWindow, Ui_frmTimeSeriesPlot):
    MAGIC = "TSGRAPHSPEC:\n"

    def __init__(self, main_form):
        self._main_form = main_form
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.rbnDate.setVisible(False)     # TODO: implement Date/Elapsed choice
        self.rbnElapsed.setVisible(False)  # TODO: implement Date/Elapsed choice
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), self.btnAdd_Clicked)
        QtCore.QObject.connect(self.btnRemove, QtCore.SIGNAL("clicked()"), self.btnRemove_Clicked)
        self.cboStart.currentIndexChanged.connect(self.cboStart_currentIndexChanged)
        self.cboEnd.currentIndexChanged.connect(self.cboEnd_currentIndexChanged)
        # self.installEventFilter(self)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        if project and self.output:
            for time_index in range(0, self.output.numPeriods):
                time_string = self.output.get_time_string(time_index)
                self.cboStart.addItem(time_string)
                self.cboEnd.addItem(time_string)
            self.cboStart.setCurrentIndex(0)
            self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)
            try:
                self.set_from_text(QtGui.QApplication.clipboard().text())
            except Exception as ex:
                print(str(ex))
                self.lstData.clear()

    def add(self, object_type, object_id, variable, axis, legend):
        item = object_type + ' ' + object_id + ' ' + variable + ' ' + axis + ' "' + legend + '"'
        self.lstData.addItem(item)

    def cboStart_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboEnd.setCurrentIndex(self.cboStart.currentIndex())

    def cboEnd_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboStart.setCurrentIndex(self.cboEnd.currentIndex())

    def btnAdd_Clicked(self):
        self._frmTimeSeriesSelection = frmTimeSeriesSelection(self._main_form)
        self._frmTimeSeriesSelection.set_from(self.project, self.output, self.add)
        self._frmTimeSeriesSelection.show()

    def btnRemove_Clicked(self):
        for item in self.lstData.selectedItems():
            self.lstData.takeItem(self.lstData.row(item))

    def cmdOK_Clicked(self):
        self.plot_time()
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.get_text(), mode=cb.Clipboard)

    def cmdCancel_Clicked(self):
        self.close()

    def get_text(self):
        return self.MAGIC + '\n'.join([str(self.lstData.item(i).text()) for i in range(self.lstData.count())])

    def set_from_text(self, text):
        if text.startswith(self.MAGIC):
            self.lstData.clear()
            for line in text[len(self.MAGIC):].split('\n'):
                self.lstData.addItem(line)

    def plot_time(self):
        fig = plt.figure()
        title = "Time Series Plot"
        fig.canvas.set_window_title(title)
        plt.title(title)
        left_y_plot = fig.add_subplot(111)
        right_y_plot = None
        left_label = None
        right_label = None
        lines = []
        line_legends = []
        x_values = []
        start_index = self.cboStart.currentIndex()
        end_index = self.cboEnd.currentIndex()
        num_steps = end_index - start_index + 1
        for time_index in range(start_index, num_steps):
            x_values.append(self.output.elapsed_hours_at_index(time_index))

        for line in [str(self.lstData.item(i).text()) for i in range(self.lstData.count())]:
            object_type, object_id, variable, axis, legend_text = line.split(None, 4)
            color = colorsys.hsv_to_rgb(np.random.rand(), 1, 1)
            legend_text = legend_text.strip('"')
            if object_type == "Node":
                item_index = self.output.get_NodeIndex(object_id)
                attribute_index = SMO.SMO_nodeAttributes[SMO.SMO_nodeAttributeNames.index(variable)]
                units = SMO.SMO_nodeAttributeUnits[attribute_index][self.output.unit_system]
                y_values = self.output.get_NodeSeries(item_index, attribute_index, start_index, num_steps)
            elif object_type == "Link":
                item_index = self.output.get_LinkIndex(object_id)
                attribute_index = SMO.SMO_linkAttributes[SMO.SMO_linkAttributeNames.index(variable)]
                units = SMO.SMO_linkAttributeUnits[attribute_index][self.output.unit_system]
                y_values = self.output.get_LinkSeries(item_index, attribute_index, start_index, num_steps)
            elif object_type == "Subcatchment":
                item_index = self.output.get_SubcatchmentIndex(object_id)
                attribute_index = SMO.SMO_subcatchAttributes[SMO.SMO_subcatchAttributeNames.index(variable)]
                units = SMO.SMO_subcatchAttributeUnits[attribute_index][self.output.unit_system]
                y_values = self.output.get_SubcatchmentSeries(item_index, attribute_index, start_index, num_steps)
            elif object_type == "System":
                attribute_index = SMO.SMO_systemAttributes[SMO.SMO_systemAttributeNames.index(variable)]
                units = SMO.SMO_systemAttributeUnits[attribute_index][self.output.unit_system]
                y_values = self.output.get_SystemSeries(item_index, attribute_index, start_index, num_steps)

            if y_values:
                if axis == "Left":
                    plot_on = left_y_plot
                else:
                    if not right_y_plot:
                        right_y_plot = fig.add_subplot(111, sharex=left_y_plot, frameon=False)
                        right_y_plot.yaxis.set_label_position("right")
                        right_y_plot.yaxis.tick_right()  # Only show right-axis tics on right axis
                        left_y_plot.yaxis.tick_left()    # Only show left-axis tics on left axis
                    plot_on = right_y_plot

                new_line = plot_on.plot(x_values, y_values, label=legend_text, c=color)[0]
                lines.append(new_line)
                line_legends.append(legend_text)
                old_label = plot_on.get_ylabel()
                if not old_label:
                    plot_on.set_ylabel(units)
                elif units not in old_label:
                    plot_on.set_ylabel(old_label + ', ' + units)

        # fig.suptitle("Time Series Plot")
        # plt.ylabel(parameter_label)
        plt.xlabel("Time (hours)")
        if not right_y_plot:
            plt.grid(True)  # Only show background grid if there is only a left Y axis
        plt.legend(lines, line_legends, loc="best")
        plt.show()

    # def keyPressEvent(self, event):
    #     if type(event) == QtGui.QKeyEvent:
    #          #here accept the event and do something
    #         print event.key()   # Key Code gets printed to the console
    #         event.accept()
    #         print(event.text())
    #
    # def eventFilter(self, obj, event):
    #     if event.type() == QtCore.QEvent.KeyPress:
    #         print "eventFilter " + event.key()   # Key Code gets printed to the console
    #         if event.key() in [QtCore.Qt.Key_Copy]:
    #             cb = QtGui.QApplication.clipboard()
    #             cb.clear(mode=cb.Clipboard)
    #             cb.setText('\n'.join([str(self.lstData.item(i).text()) for i in range(self.lstData.count())]),
    #                        mode=cb.Clipboard)
    #             return True
    #         elif event.key() in [QtCore.Qt.Key_Paste]:
    #             cb = QtGui.QApplication.clipboard()
    #             self.lstData.clear()
    #             for line in cb.getText():
    #                 self.lstData.addItem(line)
    #             return True
    #     return False
