import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.EPANET.frmEnergyReportDesigner import Ui_frmEnergyReport
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class frmEnergyReport(QtGui.QMainWindow, Ui_frmEnergyReport):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._parent = parent

    def set_data(self):
        # , nrows, ncols, headers, data):
        # counter = -1
        # self.tblGeneric.setRowCount(nrows)
        # self.tblGeneric.setColumnCount(ncols)
        # self.tblGeneric.setHorizontalHeaderLabels(headers)
        # self.tblGeneric.verticalHeader().setVisible(False)
        # for col in range(ncols):
        #     for row in range(nrows):
        #         counter += 1
        #         led = QtGui.QLineEdit(str(data[counter]))
        #         item = QtGui.QTableWidgetItem(led.text())
        #         item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #         self.tblGeneric.setItem(row,col,item)

        sc = MyMplCanvas(self.widgetChart, width=3, height=2, dpi=100)
        self.setParent(self._parent)
        self.widgetChart = sc

    def cmdCancel_Clicked(self):
        self.close()

class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        y = (0.0, 3.0, 0.01)
        x = (0,1,2)
        self.axes.plot(x, y)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)