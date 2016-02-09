import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options.general
from ui.SWMM.frmGeneralOptionsDesigner import Ui_frmGeneralOptions


class frmGeneralOptions(QtGui.QMainWindow, Ui_frmGeneralOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.swmm.options.general.General()
        section = project.find_section("OPTIONS")
        if section.ignore_rainfall == "YES":
            self.cbxRainfallRunoff.setChecked(section.ignore_rainfall)
        if section.ignore_snowmelt == "YES":
            self.cbxSnowmelt.setChecked(section.ignore_snowmelt)
        if section.ignore_groundwater == "YES":
            self.cbxGroundwater.setChecked(section.ignore_groundwater)
        if section.ignore_quality == "YES":
            self.cbxWaterQuality.setChecked(section.ignore_quality)
        if section.ignore_routing == "YES":
            self.cbxFlowRouting.setChecked(section.ignore_routing)
        if section.flow_routing == "STEADY":
            self.rbnSteady.setChecked(True)
        if section.flow_routing == "KINWAVE":
            self.rbnKinematic.setChecked(True)
        if section.flow_routing == "DYNWAVE":
            self.rbnDynamic.setChecked(True)
        if section.infiltration == "HORTON":
            self.rbnHorton.setChecked(True)
        if section.infiltration == "MODIFIED_HORTON":
            self.rbnModifiedHortonn.setChecked(True)
        if section.infiltration == "GREEN_AMPT":
            self.rbnGreenAmpt.setChecked(True)
        if section.infiltration == "MODIFIED_GREEN_AMPT":
            self.rbnModifiedGreenAmpt.setChecked(True)
        if section.infiltration == "CURVE_NUMBER":
            self.rbnCurveNumber.setChecked(True)
        self.cbxAllowPonding.setChecked(section.allow_ponding)
        self.txtMinimum.settext(section.min_slope)
        section = project.find_section("REPORT")
        self.cbxControls.setChecked(section.controls)
        self.cbxInput.setChecked(section.input)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("OPTIONS")
        section.title = self.txtTitle.toPlainText()
        if self.cbxRainfallRunoff.IsChecked:
            section.ignore_rainfall = "YES"
        else:
            section.ignore_rainfall = "NO"

        # self.cbxSnowmelt.setChecked(section.ignore_snowmelt)
        # self.cbxGroundwater.setChecked(section.ignore_groundwater)
        # self.cbxWaterQuality.setChecked(section.ignore_quality)
        # self.cbxFlowRouting.setChecked(section.ignore_routing)
        # if section.flow_routing == "STEADY":
        #     self.rbnSteady.setChecked(True)
        # if section.flow_routing == "KINWAVE":
        #     self.rbnKinematic.setChecked(True)
        # if section.flow_routing == "DYNWAVE":
        #     self.rbnDynamic.setChecked(True)
        # if section.infiltration == "HORTON":
        #     self.rbnHorton.setChecked(True)
        # if section.infiltration == "MODIFIED_HORTON":
        #     self.rbnModifiedHortonn.setChecked(True)
        # if section.infiltration == "GREEN_AMPT":
        #     self.rbnGreenAmpt.setChecked(True)
        # if section.infiltration == "MODIFIED_GREEN_AMPT":
        #     self.rbnModifiedGreenAmpt.setChecked(True)
        # if section.infiltration == "CURVE_NUMBER":
        #     self.rbnCurveNumber.setChecked(True)
        # self.cbxAllowPonding.setChecked(section.allow_ponding)
        # self.txtMinimum.settext(section.min_slope)
        # section = project.find_section("REPORT")
        # self.cbxControls.setChecked(section.controls)
        # self.cbxInput.setChecked(section.input)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()