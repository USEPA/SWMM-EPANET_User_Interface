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
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
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
            # self.tableWidget.verticalHeaderItem(row).setText('Pump ' + item)

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

        sc = MyMplCanvas(self.widgetChart, width=3, height=2, dpi=100)
        self.setParent(self._main_form)
        self.widgetChart = sc

    def cmdCancel_Clicked(self):
        self.close()

class MyMplCanvas(FigureCanvas):

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
