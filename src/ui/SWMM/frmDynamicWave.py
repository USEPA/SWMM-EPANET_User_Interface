import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options.dynamic_wave
from ui.SWMM.frmDynamicWaveDesigner import Ui_frmDynamicWave


class frmDynamicWave(QtGui.QMainWindow, Ui_frmDynamicWave):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cboInertial.addItems(("Keep", "Dampen", "Ignore"))
        # dampen=partial, ignore=full, keep=none
        self.cboForce.addItems("Hazen-Williams", "Darcy-Weisbach")
        self.cboNormal.addItems("Slope", "Froude No.", "Slope & Froude")
        self.cboThreads.addItems(("1", "2", "3", "4"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.swmm.options.dynamicwave.DynamicWave()
        section = project.find_section("OPTIONS")
        if section.inertial_damping == "PARTIAL":
            self.cboInertial.setCurrentIndex(1)
        if section.inertial_damping == "FULL":
            self.cboInertial.setCurrentIndex(2)
        if section.inertial_damping == "NONE":
            self.cboInertial.setCurrentIndex(0)
        if section.force_main_equation == "H-W":
            self.cboForce.setCurrentIndex(0)
        if section.force_main_equation == "D-W":
            self.cboForce.setCurrentIndex(1)
        if section.normal_flow_limited == "SLOPE":
            self.cboNormal.setCurrentIndex(0)
        if section.normal_flow_limited == "FROUDE":
            self.cboNormal.setCurrentIndex(1)
        if section.normal_flow_limited == "BOTH":
            self.cboNormal.setCurrentIndex(2)
        self.cboThreads.setcurrentindex(section.threads-1)
        if section.variable_step > 0:
            self.cbxUseVariable.setChecked(True)
        self.sbxAdjusted.setValue(section.variable_step * 100)
        self.txtMinimum.setText(section.minimum_step)
        self.txtLengthening.setText(section.lengthening_step)
        self.txtSurfaceArea.setText(section.min_surface_area)
        self.txtTolerance.setText(section.head_tolerance)
        self.sbxTrials.setValue(section.max_trials)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("OPTIONS")
        if self.cboInertial.CurrentIndex == 1:
            section.inertial_damping = "PARTIAL"
        if self.cboInertial.CurrentIndex == 2:
            section.inertial_damping = "FULL"
        if self.cboInertial.CurrentIndex == 0:
            section.inertial_damping = "NONE"
        if self.cboForce.CurrentIndex == 0:
            section.force_main_equation = "H-W"
        if self.cboForce.CurrentIndex == 1:
            section.force_main_equation = "D-W"
        if self.cboNormal.CurrentIndex == 0:
            section.normal_flow_limited = "SLOPE"
        if self.cboNormal.CurrentIndex == 1:
            section.normal_flow_limited = "FROUDE"
        if self.cboNormal.CurrentIndex == 2:
            section.normal_flow_limited = "BOTH"
        section.threads = self.cboThreads.currentIndex()+1
        if self.cbxUseVariable.Checked:
            section.variable_step = self.sbxAdjusted.Value / 100
        else:
            section.variable_step = 0
        section.minimum_step = self.txtMinimum.Text
        section.lengthening_step = self.txtLengthening.Text
        section.min_surface_area = self.txtSurfaceArea.Text
        section.head_tolerance = self.txtTolerance.Text
        section.max_trials = self.sbxTrials.Value
        self.close()

    def cmdCancel_Clicked(self):
        self.close()