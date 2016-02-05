import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.hydraulics
from ui.EPANET.frmHydraulicsOptionsDesigner import Ui_frmHydraulicsOptions


class frmHydraulicsOptions(QtGui.QMainWindow, Ui_frmHydraulicsOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # TODO: function that populates combo box from Enum
        self.cboFlow.addItems(("CFS", "GPM", "MGD", "IMGD", "AFD", "LPS", "LPM", "MLD", "CMH", "CMD"))
        self.cboHeadloss.addItems(("H-W", "D-W", "C-M"))
        # self.cboUnbalanced.addItems(("STOP", "CONTINUE"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.options.hydraulics.HydraulicsOptions()
        section = project.find_section("OPTIONS")
        self.cboFlow.currentText(section.flow_units)
        self.cboHeadloss.currentText(section.head_loss)
        self.txtAccuracy.setText(str(section.accuracy))
        self.txtCheckFrequency.setText(str(section.check_frequency))
        self.txtDampLimit.setText(str(section.damp_limit))
        self.txtDefaultPattern.setText(str(section.default_pattern))
        self.txtDemandMultiplier.setText(str(section.demand_multiplier))
        self.txtEmitterExponent.setText(str(section.emitter_exponent))
        self.txtMaxCheck.setText(str(section.max_check))
        self.txtMaximumTrials.setText(str(section.maximum_trials))
        self.txtRelativeViscosity.setText(str(section.relative_viscosity))
        self.txtSpecificGravity.setText(str(section.specific_gravity))
        if section.hydraulics == "USE":
            self.cbxUse.setChecked("TRUE")
        if section.hydraulics == "SAVE":
            self.cbxSave.setChecked("FALSE")
        self.txtSpecificGravity.setText(str(section.hydraulics_file))
        if section.unbalanced == "STOP":
            self.cbxStop.setChecked("TRUE")
        if section.unbalanced == "CONTINUE" and section.unbalanced_continue == 0:
            self.cbxContinue.setChecked("TRUE")
        if section.unbalanced == "CONTINUE" and section.unbalanced_continue > 0:
            self.cbxContinueN.setChecked("TRUE")
        self.cbxContinueN.setText(str(section.unbalanced_continue))

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("OPTIONS")
        # section.global_price = self.txtGlobalPrice.text()
        # section.global_pattern = self.txtGlobalPattern.text()
        # section.global_efficiency = self.txtGlobalEfficiency.text()
        # section.demand_charge = self.txtDemandCharge.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
