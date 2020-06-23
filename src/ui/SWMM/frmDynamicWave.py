import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.swmm.options.dynamic_wave
from ui.SWMM.frmDynamicWaveDesigner import Ui_frmDynamicWave
from ui.model_utility import ParseData


class frmDynamicWave(QMainWindow, Ui_frmDynamicWave):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/simulationoptions_dynamicwave.htm"
        self.setupUi(self)
        self.cboInertial.addItems(("Keep", "Dampen", "Ignore"))
        # dampen=partial, ignore=full, keep=none
        self.cboForce.addItems(("Hazen-Williams", "Darcy-Weisbach"))
        self.cboNormal.addItems(("Slope", "Froude No.", "Slope & Froude"))
        self.cboSurcharge.addItems(("Extran", "Slot"))
        self.cboThreads.addItems(("1", "2", "3", "4"))
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form
        if main_form.project.metric:
            self.lblSurface.setText("Minimum Nodal Surface Area (sq. meters)")
            self.lblHead.setText("Head Convergence Tolerance (meters)")
        else:
            self.lblSurface.setText("Minimum Nodal Surface Area (sq. feet)")
            self.lblHead.setText("Head Convergence Tolerance (feet)")

        if (main_form.program_settings.value("Geometry/" + "frmDynamicWave_geometry") and
                main_form.program_settings.value("Geometry/" + "frmDynamicWave_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmDynamicWave_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmDynamicWave_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        # section = core.swmm.options.dynamic_wave.DynamicWave()
        section = project.options.dynamic_wave
        if section.inertial_damping == core.swmm.options.dynamic_wave.InertialDamping.PARTIAL:
            self.cboInertial.setCurrentIndex(1)
        if section.inertial_damping == core.swmm.options.dynamic_wave.InertialDamping.FULL:
            self.cboInertial.setCurrentIndex(2)
        if section.inertial_damping == core.swmm.options.dynamic_wave.InertialDamping.NONE:
            self.cboInertial.setCurrentIndex(0)

        if section.force_main_equation == core.swmm.options.dynamic_wave.ForceMainEquation.H_W:
            self.cboForce.setCurrentIndex(0)
        if section.force_main_equation == core.swmm.options.dynamic_wave.ForceMainEquation.D_W:
            self.cboForce.setCurrentIndex(1)

        if section.normal_flow_limited == core.swmm.options.dynamic_wave.NormalFlowLimited.SLOPE:
            self.cboNormal.setCurrentIndex(0)
        if section.normal_flow_limited == core.swmm.options.dynamic_wave.NormalFlowLimited.FROUDE:
            self.cboNormal.setCurrentIndex(1)
        if section.normal_flow_limited == core.swmm.options.dynamic_wave.NormalFlowLimited.BOTH:
            self.cboNormal.setCurrentIndex(2)

        if section.surcharge_method == core.swmm.options.dynamic_wave.SurchargeMethod.EXTRAN:
            self.cboSurcharge.setCurrentIndex(0)
        if section.surcharge_method == core.swmm.options.dynamic_wave.SurchargeMethod.SLOT:
            self.cboSurcharge.setCurrentIndex(1)

        val, val_is_good = ParseData.intTryParse(section.threads)
        if val_is_good:
            self.cboThreads.setCurrentIndex(val - 1)
        if float(section.variable_step) > 0:
            self.cbxUseVariable.setChecked(True)
        self.sbxAdjusted.setValue(float(section.variable_step) * 100)
        self.txtMinimum.setText(str(section.minimum_step))
        self.txtLengthening.setText(str(section.lengthening_step))
        self.txtSurfaceArea.setText(str(section.min_surface_area))
        self.txtTolerance.setText(str(section.head_tolerance))
        self.sbxTrials.setValue(int(section.max_trials))

    def cmdOK_Clicked(self):
        # section = core.swmm.options.dynamic_wave.DynamicWave()
        section = self._main_form.project.options.dynamic_wave

        orig_damping = section.inertial_damping
        orig_force_eq = section.force_main_equation
        orig_flow_lim = section.normal_flow_limited
        orig_surcharge = section.surcharge_method
        orig_threads = section.threads
        orig_step = section.variable_step
        orig_min_step = section.minimum_step
        orig_len_step = section.lengthening_step
        orig_surface_area = section.min_surface_area
        orig_head_tol = section.head_tolerance
        orig_max_trials = section.max_trials

        if self.cboInertial.currentIndex() == 1:
            section.inertial_damping = core.swmm.options.dynamic_wave.InertialDamping.PARTIAL
        if self.cboInertial.currentIndex() == 2:
            section.inertial_damping = core.swmm.options.dynamic_wave.InertialDamping.FULL
        if self.cboInertial.currentIndex() == 0:
            section.inertial_damping = core.swmm.options.dynamic_wave.InertialDamping.NONE

        if self.cboForce.currentIndex() == 0:
            section.force_main_equation = core.swmm.options.dynamic_wave.ForceMainEquation.H_W
        if self.cboForce.currentIndex() == 1:
            section.force_main_equation = core.swmm.options.dynamic_wave.ForceMainEquation.D_W

        if self.cboNormal.currentIndex() == 0:
            section.normal_flow_limited = core.swmm.options.dynamic_wave.NormalFlowLimited.SLOPE
        if self.cboNormal.currentIndex() == 1:
            section.normal_flow_limited = core.swmm.options.dynamic_wave.NormalFlowLimited.FROUDE
        if self.cboNormal.currentIndex() == 2:
            section.normal_flow_limited = core.swmm.options.dynamic_wave.NormalFlowLimited.BOTH

        if self.cboSurcharge.currentIndex() == 0:
            section.surcharge_method = core.swmm.options.dynamic_wave.SurchargeMethod.EXTRAN
        if self.cboSurcharge.currentIndex() == 1:
            section.surcharge_method = core.swmm.options.dynamic_wave.SurchargeMethod.SLOT

        section.threads = self.cboThreads.currentIndex() + 1
        if self.cbxUseVariable.isChecked():
            section.variable_step = self.sbxAdjusted.value() / 100.0
        else:
            section.variable_step = 0
        section.minimum_step = float(self.txtMinimum.text())
        section.lengthening_step = float(self.txtLengthening.text())
        section.min_surface_area = float(self.txtSurfaceArea.text())
        section.head_tolerance = float(self.txtTolerance.text())
        section.max_trials = self.sbxTrials.value()

        if orig_damping != section.inertial_damping or \
            orig_force_eq != section.force_main_equation or \
            orig_flow_lim != section.normal_flow_limited or \
            orig_surcharge != section.surcharge_method or \
            int(orig_threads) != section.threads or \
            float(orig_step) != section.variable_step or \
            float(orig_min_step) != section.minimum_step or \
            float(orig_len_step) != section.lengthening_step or \
            float(orig_surface_area) != section.min_surface_area or \
            float(orig_head_tol) != section.head_tolerance or \
            int(orig_max_trials) != section.max_trials:
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmDynamicWave_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmDynamicWave_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
