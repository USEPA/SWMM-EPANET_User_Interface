import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit, QVBoxLayout, QSizePolicy
from ui.help import HelpHandler
from ui.EPANET.frmEnergyReportDesigner import Ui_frmEnergyReport
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class frmEnergyReport(QMainWindow, Ui_frmEnergyReport):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Energy_R.htm"
        self.setupUi(self)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.rbnUtilization.clicked.connect(self.rbnUtilization_Clicked)
        self.rbnAverageKw.clicked.connect(self.rbnAverageKw_Clicked)
        self.rbnCost.clicked.connect(self.rbnCost_Clicked)
        self.rbnEfficiency.clicked.connect(self.rbnEfficiency_Clicked)
        self.rbnKwHr.clicked.connect(self.rbnKwHr_Clicked)
        self.rbnPeakKw.clicked.connect(self.rbnPeakKw_Clicked)
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

            self.tableWidget.setVerticalHeaderItem(row,QTableWidgetItem('Pump ' + item))
            self.labels.append('Pump ' + item)

            led = QLineEdit(format(this_pump.utilization,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(led.text()))
            self.utilization_values.append(this_pump.utilization)

            led = QLineEdit(format(this_pump.efficiency,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 1, QTableWidgetItem(led.text()))
            self.efficiency_values.append(this_pump.efficiency)

            led = QLineEdit(format(this_pump.kw_per_flow,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 2, QTableWidgetItem(led.text()))
            self.kw_values.append(this_pump.kw_per_flow)

            led = QLineEdit(format(this_pump.average_kw,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 3, QTableWidgetItem(led.text()))
            self.average_kw_values.append(this_pump.average_kw)

            led = QLineEdit(format(this_pump.peak_kw,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 4, QTableWidgetItem(led.text()))
            self.peak_kw_values.append(this_pump.peak_kw)

            led = QLineEdit(format(this_pump.cost_per_day,'0.2f'))
            led.setReadOnly(True)
            led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.tableWidget.setItem(row, 5, QTableWidgetItem(led.text()))
            self.cost_values.append(this_pump.cost_per_day)

            cost_sum = cost_sum + this_pump.cost_per_day
            demand_charge = demand_charge + (this_pump.peak_kw * float(project.energy.demand_charge))

        self.tableWidget.setVerticalHeaderItem(row+1,QTableWidgetItem('Total Cost'))
        led = QLineEdit(format(cost_sum,'0.2f'))
        led.setReadOnly(True)
        led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.tableWidget.setItem(row+1, 5, QTableWidgetItem(led.text()))

        # demand is peak kw * demand charge
        self.tableWidget.setVerticalHeaderItem(row+2,QTableWidgetItem('Demand Charge'))
        led = QLineEdit(format(demand_charge,'0.2f'))
        led.setReadOnly(True)
        led.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.tableWidget.setItem(row+2, 5, QTableWidgetItem(led.text()))

        sc = MyMplCanvas(self.labels, self.utilization_values, self.frameChart, width=8, height=5, dpi=50)

        layout = QVBoxLayout(self.frameChart)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(sc)
        self.frameChart.setLayout(layout)

        self.setParent(self._main_form)
        self.frameChart = sc

        # set for utilization to start
        self.rbnUtilization.setChecked(True)
        self.frameChart.draw()

    def cmdCancel_Clicked(self):
        self.close()

    def rbnUtilization_Clicked(self):
        if self.rbnUtilization.isChecked():
            self.frameChart.p.cla()
            self.frameChart.p.set_title('Utilization')
            self.DoPlot(self.utilization_values)

    def rbnAverageKw_Clicked(self):
        if self.rbnAverageKw.isChecked():
            self.frameChart.p.cla()
            self.frameChart.p.set_title('Average Kw')
            self.DoPlot(self.average_kw_values)

    def rbnCost_Clicked(self):
        if self.rbnCost.isChecked():
            self.frameChart.p.cla()
            self.frameChart.p.set_title('Cost / day')
            self.DoPlot(self.cost_values)

    def rbnEfficiency_Clicked(self):
        if self.rbnEfficiency.isChecked():
            self.frameChart.p.cla()
            self.frameChart.p.set_title('Efficiency')
            self.DoPlot(self.efficiency_values)

    def rbnKwHr_Clicked(self):
        if self.rbnKwHr.isChecked():
            self.frameChart.p.cla()
            if self.output.unit_system == 0:
                self.frameChart.p.set_title('Kw-hr/Mgal')
            else:
                self.frameChart.p.set_title('Kw-hr/m3')
            self.DoPlot(self.kw_values)

    def rbnPeakKw_Clicked(self):
        if self.rbnPeakKw.isChecked():
            self.frameChart.p.cla()
            self.frameChart.p.set_title('Peak Kw')
            self.DoPlot(self.peak_kw_values)

    def DoPlot(self,values):
        import numpy as np
        ind = np.arange(len(self.labels))
        width = 0.75
        self.frameChart.p.set_xticks(ind + width/2)
        self.frameChart.p.set_xticklabels(self.labels)
        self.frameChart.p.bar(ind, values, width)
        self.frameChart.draw()


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
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
