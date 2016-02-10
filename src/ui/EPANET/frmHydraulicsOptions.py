import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.hydraulics
from enum import Enum
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

    @staticmethod
    def set_combo(combo_box, value):
        try:
            if isinstance(value, Enum):
                value = value.name
            index = combo_box.findText(value, QtCore.Qt.MatchFixedString)
            if index >= 0:
                combo_box.setCurrentIndex(index)
        except Exception as e:
            print(str(e))

    def set_from(self, project):
        hydraulics_options = project.options.hydraulics

        frmHydraulicsOptions.set_combo(self.cboFlow, hydraulics_options.flow_units)
        frmHydraulicsOptions.set_combo(self.cboHeadloss, hydraulics_options.head_loss)

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
        if hydraulics_options.hydraulics == core.epanet.options.hydraulics.Hydraulics.USE:
            self.rbnUse.setChecked(True)
            self.rbnSave.setChecked(False)
        if hydraulics_options.hydraulics == core.epanet.options.hydraulics.Hydraulics.SAVE:
            self.rbnUse.setChecked(False)
            self.rbnSave.setChecked(True)
        self.txtHydraulicsFile.setText(str(hydraulics_options.hydraulics_file))
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
        if self.cboHeadloss.currentText() == "H-W":
            head_loss_underscore = "H_W"
        elif self.cboHeadloss.currentText() == "D-W":
            head_loss_underscore = "D_W"
        else:
            head_loss_underscore = "C_M"
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
        if self.rbnUse.isChecked():
            hydraulics_options.hydraulics = core.epanet.options.hydraulics.Hydraulics.USE

        if self.rbnSave.isChecked():
            hydraulics_options.hydraulics = core.epanet.options.hydraulics.Hydraulics.SAVE

        hydraulics_options.hydraulics_file = str(self.txtHydraulicsFile.text())
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
