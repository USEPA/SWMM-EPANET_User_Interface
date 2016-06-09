import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import matplotlib.pyplot as plt
import colorsys
import datetime
import numpy as np
import core.swmm.project
import ui.convenience
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
        QtCore.QObject.connect(self.rbnDate, QtCore.SIGNAL("clicked()"), self.rbnDate_Clicked)
        QtCore.QObject.connect(self.rbnElapsed, QtCore.SIGNAL("clicked()"), self.rbnDate_Clicked)
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
            self.rbnElapsed.setChecked(True)
            self.rbnDate_Clicked()
            try:
                self.set_from_text(QtGui.QApplication.clipboard().text())
            except Exception as ex:
                print(str(ex))
                self.lstData.clear()

    def rbnDate_Clicked(self):
        self.cboStart.clear()
        self.cboEnd.clear()
        elapsed = self.rbnElapsed.isChecked()
        for time_index in range(0, self.output.numPeriods):
            if elapsed:
                time_string = self.output.get_time_string(time_index)
            else:
                time_string = self.output.get_date_string(time_index)
            self.cboStart.addItem(time_string)
            self.cboEnd.addItem(time_string)
        # if self.cboStart.currentIndex < 0:
        self.cboStart.setCurrentIndex(0)
        self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)

    def add(self, object_type, object_id, variable, axis, legend):
        item = object_type + ',' + object_id + ',' + variable + ',' + axis + ',"' + legend + '"'
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
        elapsed_flag = self.rbnElapsed.isChecked()
        start_index = self.cboStart.currentIndex()
        end_index = self.cboEnd.currentIndex()
        num_steps = end_index - start_index + 1
        lines_list = ui.convenience.all_list_items(self.lstData)
        self.plot_time(self.output, lines_list, elapsed_flag, start_index, num_steps)
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

    # TODO: move out of ui to script-accessible module
    @staticmethod
    def plot_time(output, lines_list, elapsed_flag, start_index, num_steps):
        fig = plt.figure()
        title = "Time Series Plot"
        fig.canvas.set_window_title(title)
        plt.title(title)
        left_y_plot = fig.add_subplot(111)
        right_y_plot = None
        lines_plotted = []
        line_legends = []
        x_values = []
        for time_index in range(start_index, num_steps):
            elapsed_hours = output.elapsed_hours_at_index(time_index)
            if elapsed_flag:
                x_values.append(elapsed_hours)
            else:
                x_values.append(output.StartDate + datetime.timedelta(hours=elapsed_hours))

        for line in lines_list:
            type_label, object_id, attribute, axis, legend_text = line.split(',', 4)
            legend_text = legend_text.strip('"')
            y_values, units = output.get_series_by_name(type_label, object_id, attribute, start_index, num_steps)
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

                color = colorsys.hsv_to_rgb(np.random.rand(), 1, 1)
                new_line = plot_on.plot(x_values, y_values, label=legend_text, c=color)[0]
                lines_plotted.append(new_line)
                line_legends.append(legend_text)
                old_label = plot_on.get_ylabel()
                if not old_label:
                    plot_on.set_ylabel(units)
                elif units not in old_label:
                    plot_on.set_ylabel(old_label + ', ' + units)

        # fig.suptitle("Time Series Plot")
        # plt.ylabel(parameter_label)
        if elapsed_flag:
            plt.xlabel("Time (hours)")
        else:
            plt.xlabel("Time")
        if not right_y_plot:
            plt.grid(True)  # Only show background grid if there is only a left Y axis
        plt.legend(lines_plotted, line_legends, loc="best")
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
