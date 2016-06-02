import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options.general
from ui.SWMM.frmGeneralOptionsDesigner import Ui_frmGeneralOptions


class frmGeneralOptions(QtGui.QMainWindow, Ui_frmGeneralOptions):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

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

        section = self._main_form.project.report
        section.controls = self.cbxReportControl.isChecked()
        section.input = self.cbxReportInput.isChecked()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
