from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from ui.frmPreferencesDesigner import Ui_frmPreferences

class frmPreferences(QMainWindow, Ui_frmPreferences):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.helper = HelpHandler(self)
        if main_form.model == "SWMM":
            self.help_topic = "swmm/src/src/settingprogrampreferences.htm"
        elif main_form.model == "EPANET":
            self.help_topic = "epanet/src/src/setting_.htm"
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self._main_form = main_form
        self.set_from(main_form.project)
        self.icon = main_form.windowIcon()

    def set_from(self, project):
        if self._main_form.model == "SWMM":
            self.cboSubcatchment.addItem('Precipitation')
            self.cboSubcatchment.addItem('Snow Depth')
            self.cboSubcatchment.addItem('Evaporation')
            self.cboSubcatchment.addItem('Infiltration')
            self.cboSubcatchment.addItem('Runoff')
            self.cboSubcatchment.addItem('GW Flow')
            self.cboSubcatchment.addItem('GW Elev.')
            self.cboSubcatchment.addItem('Soil Moisture')
            self.cboSubcatchment.addItem('Washoff')

            self.cboNode.addItem('Depth')
            self.cboNode.addItem('Head')
            self.cboNode.addItem('Volume')
            self.cboNode.addItem('Lateral Inflow')
            self.cboNode.addItem('Total Inflow')
            self.cboNode.addItem('Flooding')
            self.cboNode.addItem('Quality')

            self.cboLink.addItem('Flow')
            self.cboLink.addItem('Depth')
            self.cboLink.addItem('Velocity')
            self.cboLink.addItem('Volume')
            self.cboLink.addItem('Capacity')
            self.cboLink.addItem('Quality')

        elif self._main_form.model == "EPANET":
            self.lblSubcatchment.setVisible(False)
            self.cboSubcatchment.setVisible(False)
            self.lblDecimal1.setVisible(False)
            self.spnSubcatchment.setVisible(False)

            self.cboNode.addItem('Demand')
            self.cboNode.addItem('Head')
            self.cboNode.addItem('Pressure')
            self.cboNode.addItem('Quality')

            self.cboLink.addItem('Flow')
            self.cboLink.addItem('Velocity')
            self.cboLink.addItem('Unit Headloss')
            self.cboLink.addItem('Friction Factor')
            self.cboLink.addItem('Reaction Rate')
            self.cboLink.addItem('Quality')
        pass

    def cmdOK_Clicked(self):
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
