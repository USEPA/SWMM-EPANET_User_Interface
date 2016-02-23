import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.energy
from ui.EPANET.frmEnergyOptionsDesigner import Ui_frmEnergyOptions


class frmEnergyOptions(QtGui.QMainWindow, Ui_frmEnergyOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.options.energy.EnergyOptions()
        section = project.energy
        self.txtGlobalPrice.setText(str(section.global_price))
        self.txtGlobalPattern.setText(str(section.global_pattern))
        self.txtGlobalEfficiency.setText(str(section.global_efficiency))
        self.txtDemandCharge.setText(str(section.demand_charge))

    def cmdOK_Clicked(self):
        section = self._parent.project.energy
        section.global_price = self.txtGlobalPrice.text()
        section.global_pattern = self.txtGlobalPattern.text()
        section.global_efficiency = self.txtGlobalEfficiency.text()
        section.demand_charge = self.txtDemandCharge.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
