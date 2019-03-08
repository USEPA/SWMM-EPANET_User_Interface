import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.epanet.options.hydraulics
from enum import Enum
from ui.EPANET.frmHydraulicsOptionsDesigner import Ui_frmHydraulicsOptions
import ui.convenience
from ui.model_utility import ParseData


class frmHydraulicsOptions(QMainWindow, Ui_frmHydraulicsOptions):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Anal0040.htm"
        self.setupUi(self)
        self.cboFlow.clear()
        ui.convenience.set_combo_items(core.epanet.options.hydraulics.FlowUnits, self.cboFlow)
        self.cboHeadloss.addItems(("H-W", "D-W", "C-M"))
        # self.cboUnbalanced.addItems(("STOP", "CONTINUE"))
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form
        self.config = None
        if self._main_form:
            if self._main_form.project_settings:
                self.config = self._main_form.project_settings

    def set_from(self, project):
        hydraulics_options = project.options.hydraulics

        ui.convenience.set_combo(self.cboFlow, hydraulics_options.flow_units)
        ui.convenience.set_combo(self.cboHeadloss, hydraulics_options.head_loss.name.replace('_', "-"))

        self.txtAccuracy.setText(str(hydraulics_options.accuracy))
        self.txtCheckFrequency.setText(str(hydraulics_options.check_frequency))
        self.txtDampLimit.setText(str(hydraulics_options.damp_limit))
        self.txtDefaultPattern.setText(str(hydraulics_options.default_pattern))
        self.txtDemandMultiplier.setText(str(hydraulics_options.demand_multiplier))
        self.txtEmitterExponent.setText(str(hydraulics_options.emitter_exponent))
        self.txtMaxCheck.setText(str(hydraulics_options.max_check))
        self.txtMaximumTrials.setText(str(hydraulics_options.maximum_trials))
        self.txtRelativeViscosity.setText(str(hydraulics_options.viscosity))
        self.txtSpecificGravity.setText(str(hydraulics_options.specific_gravity))
        if hydraulics_options.unbalanced == core.epanet.options.hydraulics.Unbalanced.STOP:
            self.rbnStop.setChecked(True)
        if hydraulics_options.unbalanced == core.epanet.options.hydraulics.Unbalanced.CONTINUE:
            val, val_is_good = ParseData.intTryParse(hydraulics_options.unbalanced_continue)
            if not val_is_good:
                val = 0
            if val == 0:
                self.rbnContinue.setChecked(True)
            elif val > 0:
                self.rbnContinueN.setChecked(True)
        self.txtContinueN.setText(str(hydraulics_options.unbalanced_continue))

    def cmdOK_Clicked(self):
        hydraulics_options = self._main_form.project.options.hydraulics

        if hydraulics_options.flow_units != core.epanet.options.hydraulics.FlowUnits[self.cboFlow.currentText()] :
            self._main_form.mark_project_as_unsaved()

        hydraulics_options.flow_units = core.epanet.options.hydraulics.FlowUnits[self.cboFlow.currentText()]
        ui.convenience.set_combo(self._main_form.cbFlowUnits, 'Flow Units: ' + hydraulics_options.flow_units.name)
        head_loss_underscore = self.cboHeadloss.currentText().replace('-', '_')

        if hydraulics_options.head_loss != core.epanet.options.hydraulics.HeadLoss[head_loss_underscore] or \
            hydraulics_options.accuracy != float(self.txtAccuracy.text()) or \
            hydraulics_options.check_frequency != int(self.txtCheckFrequency.text()) or \
            hydraulics_options.damp_limit != float(self.txtDampLimit.text()) or \
            hydraulics_options.default_pattern != self.txtDefaultPattern.text() or \
            hydraulics_options.demand_multiplier != float(self.txtDemandMultiplier.text()) or \
            hydraulics_options.emitter_exponent != float(self.txtEmitterExponent.text()) or \
            hydraulics_options.max_check != int(self.txtMaxCheck.text()) or \
            hydraulics_options.maximum_trials != int(self.txtMaximumTrials.text()) or \
            hydraulics_options.viscosity != float(self.txtRelativeViscosity.text()) or \
            hydraulics_options.specific_gravity != float(self.txtSpecificGravity.text() or \
            hydraulics_options.unbalanced_continue != self.txtContinueN.text()):
            self._main_form.mark_project_as_unsaved()

        hydraulics_options.head_loss = core.epanet.options.hydraulics.HeadLoss[head_loss_underscore]
        hydraulics_options.accuracy = float(self.txtAccuracy.text())
        hydraulics_options.check_frequency = int(self.txtCheckFrequency.text())
        hydraulics_options.damp_limit = float(self.txtDampLimit.text())
        hydraulics_options.default_pattern = self.txtDefaultPattern.text()
        hydraulics_options.demand_multiplier = float(self.txtDemandMultiplier.text())
        hydraulics_options.emitter_exponent = float(self.txtEmitterExponent.text())
        hydraulics_options.max_check = int(self.txtMaxCheck.text())
        hydraulics_options.maximum_trials = int(self.txtMaximumTrials.text())
        hydraulics_options.viscosity = float(self.txtRelativeViscosity.text())
        hydraulics_options.specific_gravity = float(self.txtSpecificGravity.text())

        orig_unbalanced = hydraulics_options.unbalanced
        if self.rbnStop.isChecked():
            hydraulics_options.unbalanced = core.epanet.options.hydraulics.Unbalanced.STOP
        if self.rbnContinue.isChecked():
            hydraulics_options.unbalanced = core.epanet.options.hydraulics.Unbalanced.CONTINUE
            hydraulics_options.unbalanced_continue = 0
        elif self.rbnContinueN.isChecked():
            hydraulics_options.unbalanced = core.epanet.options.hydraulics.Unbalanced.CONTINUE
            hydraulics_options.unbalanced_continue = self.txtContinueN.text()

        if hydraulics_options.unbalanced != orig_unbalanced:
            self._main_form.mark_project_as_unsaved()

        if self.config:
            self.sync_hydraulic_settings()
        self.close()

    def sync_hydraulic_settings(self):
        """
        sync hydraulic options into project settings
        """
        if not self.config: return
        #from ui.EPANET.inifile import DefaultsEPANET
        #self.config = DefaultsEPANET()
        hydraulics_options = self._main_form.project.options.hydraulics
        for key in self.config.parameters_keys:
            if "flow units" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.flow_units.name
            elif "headloss" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.head_loss.name
            elif "unbalanced" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.unbalanced.name
            elif "accuracy" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.accuracy
            elif "check freq" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.check_frequency
            elif "damp" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.damp_limit
            elif "pattern" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.default_pattern
            elif "demand" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.demand_multiplier
            elif "emitter" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.emitter_exponent
            elif "max check" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.max_check
            elif "trial" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.maximum_trials
            elif "viscosity" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.viscosity
            elif "gravity" in key.lower():
                self.config.parameters_values[key] = hydraulics_options.specific_gravity
            #elif "continue n" in key.lower():
            #    hydraulics_options.unbalanced_continue = 0

    def cmdCancel_Clicked(self):
        self.close()
