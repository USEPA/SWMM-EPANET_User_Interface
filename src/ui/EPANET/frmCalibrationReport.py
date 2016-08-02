import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui.EPANET.frmCalibrationReportDesigner import Ui_frmCalibrationReport


class frmCalibrationReport(QtGui.QMainWindow, Ui_frmCalibrationReport):

    def __init__(self, main_form, calibrate_against, node_id):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Cali0078.htm"
        self.setupUi(self)
        # QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.setWindowTitle('EPANET Calibration Report - ' + calibrate_against)
        self._main_form = main_form

        heading = ' Calibration Statistics for ' + calibrate_against + '\n' \
                + '\n' \
                + '                Num    Observed    Computed    Mean     RMS' + '\n' \
                + '  Location      Obs        Mean        Mean   Error   Error' + '\n' \
                + '  ---------------------------------------------------------' + '\n' \
                + '  11              9        0.64      148.43 147.794 154.996' + '\n' \
                + '  ---------------------------------------------------------' + '\n' \
                + '  Network         9        0.64      148.43 147.794 154.996' + '\n' \
                + '\n' \
                + '  Correlation Between Means: -1.452'

        self.txtStatistics.setReadOnly(True)
        self.txtStatistics.setText(heading)

        # correlation plot tab
        correlation_plot = MyPlot(self.widgetPlot, width=6, height=2, dpi=100)
        self.setParent(self._main_form)
        self.widgetPlot = correlation_plot

        # mean comparisons tab
        mean_plot = MyPlot(self.widgetMean, width=6, height=2, dpi=100)
        self.setParent(self._main_form)
        self.widgetMean = mean_plot

    def cmdCancel_Clicked(self):
        self.close()

class MyPlot(FigureCanvas):

    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        y = (0.0, 3.0, 0.01)
        x = (0,1,2)
        self.axes.plot(x, y)

        FigureCanvas.__init__(self, fig)
        self.setParent(main_form)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
