from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from ui.help import HelpHandler
from frmPlotViewerDesigner import Ui_frmPlot
import matplotlib as mp
from model_utility import ParseData
from model_utility import BasePlot
import numpy as np


class frmPlotViewer(QtGui.QMainWindow, Ui_frmPlot):
    """
    Generic plot viewer window that can copy, save, and print a plot
    - Time Series Viewer
    """

    MAGIC = "TSGRAPHSPEC:"

    def __init__(self, dataset):
        """
        Constructor
        Args:
            dataset: time series data as pandas data frame
        """
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.dataset = dataset
        self.plot_type = 'timeseries'
        self.plot = CurvePlot(self.fraPlot, width=6, height=2, dpi=100)
        layout = QtGui.QVBoxLayout(self.fraPlot)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot)
        self.fraPlot.setLayout(layout)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/timeseriesplotdialog.htm"
        self.Xunits = {}
        self.Yunits = {}
        self.Xlabel = ""
        self.Ylabel = ""
        self.Xunit = ""
        self.Yunit = ""
        self.TXT_OPEN_CURVE_TITLE = 'Open a Curve'
        self.TXT_SAVE_CURVE_TITLE = 'Save Curve As'
        self.TXT_CURVE_FILTER = 'Curve files (*.CRV)|*.CRV|All files|*.*'
        self.TXT_CURVE_HEADER = 'EPANET Curve Data'
        self.xvals = []
        self.yvals = []
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL("clicked()"), self.frm_close)
        QtCore.QObject.connect(self.btnHelp, QtCore.SIGNAL("clicked()"), self.get_help)
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open_datafile)
        QtCore.QObject.connect(self.actionCopy, QtCore.SIGNAL("triggered()"), self.copy_plot)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL("triggered()"), self.save_plot)
        QtCore.QObject.connect(self.actionPrint, QtCore.SIGNAL("triggered()"), self.print_plot)
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
            self.plot.set_data(self.dataset)
        pass

    def frm_close(self):
        """
        Close the plot form and discard dataset
        Returns:

        """
        self.close()

    def get_help(self):
        pass


class CurvePlot(BasePlot):
    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        BasePlot.__init__(self, main_form, width, height, dpi)
        self.line, = self.axes.plot([],[], 'r-')
        pass

    def setData(self, X, Y, Xlabel, Ylabel, good_pump_curve):
        color = self.get_colors()
        #self.axes.scatter(self.X, self.Y, s=10, c=color, marker="o", label="")
        #self.axes.legend(loc='upper left')
        self.line.set_xdata(X)
        self.line.set_ydata(Y)
        if good_pump_curve:
            self.line.set_marker(None)
        else:
            self.line.set_marker("s")
            self.line.set_markeredgecolor("black")
            self.line.set_markerfacecolor("green")

        self.setXlabel(Xlabel)
        self.setYlabel(Ylabel)
        self.axes.relim()
        self.axes.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        #self.setTitle('Pump head curve for %s' % aData.name)
        pass

    def set_data(self, df):
        self.axes = df.plot()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        pass

    def get_colors(self):
        return QColor("blue")