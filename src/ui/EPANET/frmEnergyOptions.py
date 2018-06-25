import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.epanet.options.energy
from ui.EPANET.frmEnergyOptionsDesigner import Ui_frmEnergyOptions


class frmEnergyOptions(QMainWindow, Ui_frmEnergyOptions):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Anal0030.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        # section = core.epanet.options.energy.EnergyOptions()
        section = project.energy
        self.txtGlobalPrice.setText(str(section.global_price))
        self.txtGlobalPattern.setText(str(section.global_pattern))
        self.txtGlobalEfficiency.setText(str(section.global_efficiency))
        self.txtDemandCharge.setText(str(section.demand_charge))

    def cmdOK_Clicked(self):
        section = self._main_form.project.energy
        section.global_price = self.txtGlobalPrice.text()
        section.global_pattern = self.txtGlobalPattern.text()
        section.global_efficiency = self.txtGlobalEfficiency.text()
        section.demand_charge = self.txtDemandCharge.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
