import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.EPANET.frmEnergyReportDesigner import Ui_frmEnergyReport


class frmEnergyReport(QtGui.QMainWindow, Ui_frmEnergyReport):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._parent = parent

    def set_data(self, nrows, ncols, headers, data):
        counter = -1
        self.tblGeneric.setRowCount(nrows)
        self.tblGeneric.setColumnCount(ncols)
        self.tblGeneric.setHorizontalHeaderLabels(headers)
        self.tblGeneric.verticalHeader().setVisible(False)
        for col in range(ncols):
            for row in range(nrows):
                counter += 1
                led = QtGui.QLineEdit(str(data[counter]))
                item = QtGui.QTableWidgetItem(led.text())
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tblGeneric.setItem(row,col,item)

    def cmdCancel_Clicked(self):
        self.close()
