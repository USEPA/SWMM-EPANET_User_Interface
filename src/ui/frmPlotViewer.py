from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from ui.help import HelpHandler
from .frmPlotViewerDesigner import Ui_frmPlot
import matplotlib.dates as mdates
from .model_utility import ParseData
from .model_utility import BasePlot
import numpy as np
from datetime import datetime


class frmPlotViewer(QMainWindow, Ui_frmPlot):
    """
    Generic plot viewer window that can copy, save, and print a plot
    - Time Series Viewer
    """

    # MAGIC = "TSGRAPHSPEC:"

    def __init__(self, dataset, plot_type, plot_title, window_icon, x_title, y_title):
        """
        Constructor
        Args:
            dataset: time series data as pandas data frame
        """
        QMainWindow.__init__(self)
        self.helper = HelpHandler(self)
        self.setupUi(self)
        self.setWindowIcon(window_icon)

        self.actionPrint.setVisible(False)
        self.actionSave.setVisible(False)
        self.actionCopy.setVisible(False)
        self.menuFile.setEnabled(False)
        self.menuFile.setVisible(False)
        self.menuFile.deleteLater()

        self.dataset = dataset
        self.plot_title = plot_title
        self.x_title = x_title
        self.y_title = y_title
        if plot_type == 'time':
            self.plot_type = 'timeseries'
            self.help_topic = "swmm/src/src/timeserieseditordialog.htm"
        elif plot_type == 'xy':
            self.plot_type = 'xy'
            self.help_topic = "swmm/src/src/transecteditordialog.htm"
        self.plot = CurvePlot(self.fraPlot, width=6, height=2, dpi=100)
        layout = QVBoxLayout(self.fraPlot)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot)
        self.fraPlot.setLayout(layout)
        self.helper = HelpHandler(self)

        self.Xunits = {}
        self.Yunits = {}
        self.Xlabel = ""
        self.Ylabel = ""
        self.Xunit = ""
        self.Yunit = ""
        self.TXT_OPEN_CURVE_TITLE = 'Open a Curve'
        self.TXT_SAVE_CURVE_TITLE = 'Save Curve As'
        self.TXT_CURVE_FILTER = 'Curve files (*.CRV)|*.CRV|All files|*.*'
        self.xvals = []
        self.yvals = []
        self.btnClose.clicked.connect(self.frm_close)
        self.btnHelp.clicked.connect(self.get_help)
        self.actionOpen.triggered.connect(self.open_datafile)
        self.actionCopy.triggered.connect(self.copy_plot)
        self.actionSave.triggered.connect(self.save_plot)
        self.actionPrint.triggered.connect(self.print_plot)
        # self.installEventFilter(self)
        self.do_plot()

    def open_datafile(self):
        pass

    def copy_plot(self):
        pass

    def save_plot(self):
        pass

    def print_plot(self):
        pass

    def do_plot(self):
        """
        Construct a plot of the dataset
        ToDo: based on user-specified plot type
        Returns:

        """
        if self.dataset.shape[0] > 0 and self.dataset.shape[1] > 0:
            self.plot.setTitle(self.plot_title)
            if self.plot_type == 'timeseries':
                self.plot.set_time_series_data(self.dataset)
            elif self.plot_type == 'xy':
                self.plot.set_xy_data(self.dataset, self.x_title, self.y_title)

        pass

    def frm_close(self):
        """
        Close the plot form and discard dataset
        Returns:

        """
        self.close()

    def get_help(self):
        self.helper.show_help()


class CurvePlot(BasePlot):
    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        BasePlot.__init__(self, main_form, width, height, dpi)
        self.line, = self.axes.plot([],[], 'r-')
        pass

    def setData(self, X, Y, Xlabel, Ylabel):
        color = self.get_colors()
        #self.axes.scatter(self.X, self.Y, s=10, c=color, marker="o", label="")
        #self.axes.legend(loc='upper left')
        self.line.set_xdata(X)
        self.line.set_ydata(Y)
        self.line.set_marker("o")
        self.line.set_markeredgecolor("blue")
        self.line.set_markerfacecolor("lightblue")

        self.setXlabel(Xlabel)
        self.setYlabel(Ylabel)
        self.axes.relim()
        self.axes.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        #self.setTitle('Pump head curve for %s' % aData.name)
        pass

    def set_time_series_data(self, df):
        #self.line, = self.axes.plot_date(x=[],y=[])
        if df.shape[0] > 0 and df.shape[1] > 0:
            x = []
            y = []
            for row in range(len(df)):
                #ts = self.dataset.index[row]
                #self.xvals.append(datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second))
                if df.hour_only:
                    x.append(df.index[row])
                else:
                    x.append(mdates.date2num(df.index[row]))
                y.append(df.iloc[row][0])

            if df.hour_only:
                self.setData(x, y, "Elapsed time (hours)", "")
            else:
                self.axes.plot_date(x, y, 'b-', marker='o', markeredgecolor='blue',
                                markerfacecolor='lightblue')
                self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y\n%H:%M'))
                self.setXlabel("Elapsed time (date)")
                self.setYlabel("")
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def set_xy_data(self, df, x_title, y_title):
        if df.shape[0] > 0 and df.shape[1] > 0:
            x = []
            y = []
            for row in range(len(df)):
                x.append(float(df.index[row]))
                y.append(float(df.iloc[row][0]))
            self.setData(x, y, x_title, y_title)

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def set_data(self, df, **kwargs):
        df.plot(ax=self.axes)
        self.draw()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        pass



    def get_colors(self):
        return QColor("blue")
