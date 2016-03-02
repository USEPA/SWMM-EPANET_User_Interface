import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.hydraulics
from enum import Enum
from ui.EPANET.frmHydraulicsOptionsDesigner import Ui_frmHydraulicsOptions
import ui.convenience


class frmHydraulicsOptions(QtGui.QMainWindow, Ui_frmHydraulicsOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cboFlow.clear()
        ui.convenience.set_combo_items(core.epanet.options.hydraulics.FlowUnits, self.cboFlow)
        self.cboHeadloss.addItems(("H-W", "D-W", "C-M"))
        # self.cboUnbalanced.addItems(("STOP", "CONTINUE"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

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
            if hydraulics_options.unbalanced_continue == 0:
                self.rbnContinue.setChecked(True)
            elif hydraulics_options.unbalanced_continue > 0:
                self.rbnContinueN.setChecked(True)
        self.txtContinueN.setText(str(hydraulics_options.unbalanced_continue))

    def cmdOK_Clicked(self):
        hydraulics_options = self._parent.project.options.hydraulics
        hydraulics_options.flow_units = core.epanet.options.hydraulics.FlowUnits[self.cboFlow.currentText()]
        head_loss_underscore = self.cboHeadloss.currentText().replace('-', '_')
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
        if self.rbnStop.isChecked():
            hydraulics_options.unbalanced = core.epanet.options.hydraulics.Unbalanced.STOP
        if self.rbnContinue.isChecked():
            hydraulics_options.unbalanced = core.epanet.options.hydraulics.Unbalanced.CONTINUE
            hydraulics_options.unbalanced_continue = 0
        elif self.rbnContinueN.isChecked():
            hydraulics_options.unbalanced = core.epanet.options.hydraulics.Unbalanced.CONTINUE
            hydraulics_options.unbalanced_continue = self.txtContinueN.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
