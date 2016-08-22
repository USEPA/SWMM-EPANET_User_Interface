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
        self.labels = []
        self.utilization_values = []
        self.efficiency_values = []
        self.kw_values = []
        self.average_kw_values = []
        self.peak_kw_values = []
        self.cost_values = []

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
            self.labels.append('Pump ' + item)

            led = QtGui.QLineEdit(format(this_pump.utilization,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 0, QtGui.QTableWidgetItem(led.text()))
            self.utilization_values.append(this_pump.utilization)

            led = QtGui.QLineEdit(format(this_pump.efficiency,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 1, QtGui.QTableWidgetItem(led.text()))
            self.efficiency_values.append(this_pump.efficiency)

            led = QtGui.QLineEdit(format(this_pump.kw_per_flow,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 2, QtGui.QTableWidgetItem(led.text()))
            self.kw_values.append(this_pump.kw_per_flow)

            led = QtGui.QLineEdit(format(this_pump.average_kw,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 3, QtGui.QTableWidgetItem(led.text()))
            self.average_kw_values.append(this_pump.average_kw)

            led = QtGui.QLineEdit(format(this_pump.peak_kw,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 4, QtGui.QTableWidgetItem(led.text()))
            self.peak_kw_values.append(this_pump.peak_kw)

            led = QtGui.QLineEdit(format(this_pump.cost_per_day,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 5, QtGui.QTableWidgetItem(led.text()))
            self.cost_values.append(this_pump.cost_per_day)

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

        sc = MyMplCanvas(self.labels, self.utilization_values, self.widgetChart, width=8, height=5, dpi=50)
        self.setParent(self._main_form)
        self.widgetChart = sc

        # set for utilization to start
        self.rbnUtilization.setChecked(True)
        self.widgetChart.draw()

    def cmdCancel_Clicked(self):
        self.close()

    def rbnUtilization_Clicked(self):
        if self.rbnUtilization.isChecked():
            self.widgetChart.p.cla()
            self.widgetChart.p.set_title('Utilization')
            self.DoPlot(self.utilization_values)

    def rbnAverageKw_Clicked(self):
        if self.rbnAverageKw.isChecked():
            self.widgetChart.p.cla()
            self.widgetChart.p.set_title('Average Kw')
            self.DoPlot(self.average_kw_values)

    def rbnCost_Clicked(self):
        if self.rbnCost.isChecked():
            self.widgetChart.p.cla()
            self.widgetChart.p.set_title('Cost / day')
            self.DoPlot(self.cost_values)

    def rbnEfficiency_Clicked(self):
        if self.rbnEfficiency.isChecked():
            self.widgetChart.p.cla()
            self.widgetChart.p.set_title('Efficiency')
            self.DoPlot(self.efficiency_values)

    def rbnKwHr_Clicked(self):
        if self.rbnKwHr.isChecked():
            self.widgetChart.p.cla()
            if self.output.unit_system == 0:
                self.widgetChart.p.set_title('Kw-hr/Mgal')
            else:
                self.widgetChart.p.set_title('Kw-hr/m3')
            self.DoPlot(self.kw_values)

    def rbnPeakKw_Clicked(self):
        if self.rbnPeakKw.isChecked():
            self.widgetChart.p.cla()
            self.widgetChart.p.set_title('Peak Kw')
            self.DoPlot(self.peak_kw_values)

    def DoPlot(self,values):
        import numpy as np
        ind = np.arange(len(self.labels))
        width = 0.75
        self.widgetChart.p.set_xticks(ind + width/2)
        self.widgetChart.p.set_xticklabels(self.labels)
        self.widgetChart.p.bar(ind, values, width)
        self.widgetChart.draw()

class MyMplCanvas(FigureCanvas):

    def __init__(self, labels, values, main_form=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.p = fig.gca()

        import numpy as np
        ind = np.arange(len(labels))
        width = 0.75
        self.p.set_xticks(ind + width/2)
        self.p.set_xticklabels(labels)
        self.p.set_title('Utilization')
        self.p.bar(ind, values, width)

        FigureCanvas.__init__(self, fig)
        self.setParent(main_form)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
