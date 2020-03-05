import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.swmm.options.general
from ui.SWMM.frmGeneralOptionsDesigner import Ui_frmGeneralOptions


class frmGeneralOptions(QMainWindow, Ui_frmGeneralOptions):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/simulationoptions_general.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmGeneralOptions_geometry") and
                main_form.program_settings.value("Geometry/" + "frmGeneralOptions_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmGeneralOptions_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmGeneralOptions_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        # section = core.swmm.options.general.General()
        section = project.options
        self.cbxRainfallRunoff.setChecked(not section.ignore_rainfall)
        self.cbxRainfallII.setChecked(not section.ignore_rdii)
        self.cbxSnowmelt.setChecked(not section.ignore_snowmelt)
        self.cbxGroundwater.setChecked(not section.ignore_groundwater)
        self.cbxWaterQuality.setChecked(not section.ignore_quality)
        self.cbxFlowRouting.setChecked(not section.ignore_routing)

        if section.flow_routing == core.swmm.options.general.FlowRouting.STEADY:
            self.rbnSteady.setChecked(True)
        if section.flow_routing == core.swmm.options.general.FlowRouting.KINWAVE:
            self.rbnKinematic.setChecked(True)
        if section.flow_routing == core.swmm.options.general.FlowRouting.DYNWAVE:
            self.rbnDynamic.setChecked(True)

        if section.infiltration == "HORTON":
            self.rbnHorton.setChecked(True)
        if section.infiltration == "MODIFIED_HORTON":
            self.rbnModifiedHorton.setChecked(True)
        if section.infiltration == "GREEN_AMPT":
            self.rbnGreenAmpt.setChecked(True)
        if section.infiltration == "MODIFIED_GREEN_AMPT":
            self.rbnModifiedGreenAmpt.setChecked(True)
        if section.infiltration == "CURVE_NUMBER":
            self.rbnCurveNumber.setChecked(True)

        self.cbxAllowPonding.setChecked(section.allow_ponding)
        self.txtMinimum.setText(str(section.min_slope))

        self.cbxReportControl.setChecked(project.report.controls)
        self.cbxReportInput.setChecked(project.report.input)

    def cmdOK_Clicked(self):
        section = self._main_form.project.options

        orig_ignore_rainfall = section.ignore_rainfall
        orig_ignore_rdii = section.ignore_rdii
        orig_ignore_snowmelt = section.ignore_snowmelt
        orig_ignore_groundwater = section.ignore_groundwater
        orig_ignore_quality = section.ignore_quality
        orig_ignore_routing = section.ignore_routing
        orig_flow_routing = section.flow_routing
        orig_infiltration = section.infiltration
        orig_allow_ponding = section.allow_ponding
        orig_min_slope = section.min_slope

        section.ignore_rainfall = not self.cbxRainfallRunoff.isChecked()
        section.ignore_rdii = not self.cbxRainfallII.isChecked()
        section.ignore_snowmelt = not self.cbxSnowmelt.isChecked()
        section.ignore_groundwater = not self.cbxGroundwater.isChecked()
        section.ignore_quality = not self.cbxWaterQuality.isChecked()
        section.ignore_routing = not self.cbxFlowRouting.isChecked()

        if self.rbnSteady.isChecked():
            section.flow_routing = core.swmm.options.general.FlowRouting.STEADY
        if self.rbnKinematic.isChecked():
            section.flow_routing = core.swmm.options.general.FlowRouting.KINWAVE
        if self.rbnDynamic.isChecked():
            section.flow_routing = core.swmm.options.general.FlowRouting.DYNWAVE

        if self.rbnHorton.isChecked():
            section.infiltration = "HORTON"
        if self.rbnModifiedHorton.isChecked():
            section.infiltration = "MODIFIED_HORTON"
        if self.rbnGreenAmpt.isChecked():
            section.infiltration = "GREEN_AMPT"
        if self.rbnModifiedGreenAmpt.isChecked():
            section.infiltration = "MODIFIED_GREEN_AMPT"
        if self.rbnCurveNumber.isChecked():
            section.infiltration = "CURVE_NUMBER"

        section.allow_ponding = self.cbxAllowPonding.isChecked()
        section.min_slope = float(self.txtMinimum.text())

        if orig_ignore_rainfall != section.ignore_rainfall or \
            orig_ignore_rdii != section.ignore_rdii or \
            orig_ignore_snowmelt != section.ignore_snowmelt or \
            orig_ignore_groundwater != section.ignore_groundwater or \
            orig_ignore_quality != section.ignore_quality or \
            orig_ignore_routing != section.ignore_routing or \
            orig_flow_routing != section.flow_routing or \
            orig_infiltration != section.infiltration or \
            orig_allow_ponding != section.allow_ponding or \
            float(orig_min_slope) != section.min_slope:
            self._main_form.mark_project_as_unsaved()

        section = self._main_form.project.report

        orig_controls = section.controls
        orig_input = section.input

        section.controls = self.cbxReportControl.isChecked()
        section.input = self.cbxReportInput.isChecked()

        if orig_controls != section.controls or \
            orig_input != section.input:
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmGeneralOptions_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmGeneralOptions_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmGeneralOptions_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmGeneralOptions_state", self.saveState())
        self.close()
