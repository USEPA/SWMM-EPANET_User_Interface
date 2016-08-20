import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
from ui.EPANET.frmEnergyReportDesigner import Ui_frmEnergyReport
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class frmEnergyReport(QtGui.QMainWindow, Ui_frmEnergyReport):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Energy_R.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.rbnUtilization, QtCore.SIGNAL("clicked()"), self.rbnUtilization_Clicked)
        QtCore.QObject.connect(self.rbnAverageKw, QtCore.SIGNAL("clicked()"), self.rbnAverageKw_Clicked)
        QtCore.QObject.connect(self.rbnCost, QtCore.SIGNAL("clicked()"), self.rbnCost_Clicked)
        QtCore.QObject.connect(self.rbnEfficiency, QtCore.SIGNAL("clicked()"), self.rbnEfficiency_Clicked)
        QtCore.QObject.connect(self.rbnKwHr, QtCore.SIGNAL("clicked()"), self.rbnKwHr_Clicked)
        QtCore.QObject.connect(self.rbnPeakKw, QtCore.SIGNAL("clicked()"), self.rbnPeakKw_Clicked)
        self._main_form = main_form

    def set_data(self, project, output):
        self.project = project
        self.output = output

        # Get flow volume units of Kw-hr per unit of flow
        # (Mil. gal. for US units, cubic meters for SI)
        if (self.output.unit_system == 0):
            self.tableWidget.horizontalHeaderItem(2).setText('Kw-hr/Mgal')
        else:
            self.tableWidget.horizontalHeaderItem(2).setText('Kw-hr/m3')

        all_pump_energy = output.get_pump_energy_usage_statistics()

        self.tableWidget.setRowCount(len(all_pump_energy)+2)

        row = -1
        cost_sum = 0.0
        demand_charge = 0.0
        for item in all_pump_energy:
            row += 1
            this_pump = all_pump_energy[item]

            self.tableWidget.setVerticalHeaderItem(row,QtGui.QTableWidgetItem('Pump ' + item))

            led = QtGui.QLineEdit(format(this_pump.utilization,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 0, QtGui.QTableWidgetItem(led.text()))

            led = QtGui.QLineEdit(format(this_pump.efficiency,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 1, QtGui.QTableWidgetItem(led.text()))

            led = QtGui.QLineEdit(format(this_pump.kw_per_flow,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 2, QtGui.QTableWidgetItem(led.text()))

            led = QtGui.QLineEdit(format(this_pump.average_kw,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 3, QtGui.QTableWidgetItem(led.text()))

            led = QtGui.QLineEdit(format(this_pump.peak_kw,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 4, QtGui.QTableWidgetItem(led.text()))

            led = QtGui.QLineEdit(format(this_pump.cost_per_day,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 5, QtGui.QTableWidgetItem(led.text()))

            cost_sum = cost_sum + this_pump.cost_per_day
            demand_charge = demand_charge + (this_pump.peak_kw * float(project.energy.demand_charge))

        self.tableWidget.setVerticalHeaderItem(row+1,QtGui.QTableWidgetItem('Total Cost'))
        led = QtGui.QLineEdit(format(cost_sum,'0.2f'))
        led.setReadOnly(True)
        led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.tableWidget.setItem(row+1, 5, QtGui.QTableWidgetItem(led.text()))

        # demand is peak kw * demand charge
        self.tableWidget.setVerticalHeaderItem(row+2,QtGui.QTableWidgetItem('Demand Charge'))
        led = QtGui.QLineEdit(format(demand_charge,'0.2f'))
        led.setReadOnly(True)
        led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.tableWidget.setItem(row+2, 5, QtGui.QTableWidgetItem(led.text()))

        self.rbnUtilization.setChecked(True)
        sc = MyMplCanvas('Utilization', self.widgetChart, width=8, height=5, dpi=50)
        self.setParent(self._main_form)
        self.widgetChart = sc

    def DoPlot(self,title):
        sc = MyMplCanvas(title, self.widgetChart, width=8, height=5, dpi=50)
        self.setParent(self._main_form)
        self.widgetChart = sc

    def cmdCancel_Clicked(self):
        self.close()

    def rbnUtilization_Clicked(self):
        if self.rbnUtilization.isChecked():
            self.DoPlot('Utilization')

    def rbnAverageKw_Clicked(self):
        if self.rbnAverageKw.isChecked():
            self.DoPlot('AverageKw')

    def rbnCost_Clicked(self):
        if self.rbnCost.isChecked():
            self.DoPlot('Cost')

    def rbnEfficiency_Clicked(self):
        if self.rbnEfficiency.isChecked():
            self.DoPlot('Efficiency')

    def rbnKwHr_Clicked(self):
        if self.rbnKwHr.isChecked():
            self.DoPlot('KwHr')

    def rbnPeakKw_Clicked(self):
        if self.rbnPeakKw.isChecked():
            self.DoPlot('PeakKw')

class MyMplCanvas(FigureCanvas):

    def __init__(self, title, main_form=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        p = fig.gca()

        import numpy as np
        N = 5
        values = (20, 35, 30, 35, 27)
        ind = np.arange(N)
        width = 0.75

        p.set_title(title)
        p.set_xticks(ind + width/2)
        p.set_xticklabels(('Pump 1', 'Pump 2', 'Pump 3', 'Pump 4', 'Pump 5'))

        p.bar(ind, values, width)

        FigureCanvas.__init__(self, fig)
        self.setParent(main_form)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
