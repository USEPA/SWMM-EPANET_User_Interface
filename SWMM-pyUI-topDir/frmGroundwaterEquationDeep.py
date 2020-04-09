import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from frmGroundwaterEquationDeepDesigner import Ui_frmGroundwaterEquationDeep
from core.swmm.hydrology.subcatchment import GWF, GroundwaterFlowType


class frmGroundwaterEquationDeep(QMainWindow, Ui_frmGroundwaterEquationDeep):

    def __init__(self, main_form, subcatchment_name):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/groundwater_equation_editor.htm"
        self._main_form = main_form
        self.setupUi(self)
        self.subcatchment_name = subcatchment_name
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)

        if (main_form.program_settings.value("Geometry/" + "frmGroundwaterEquationDeep_geometry") and
                main_form.program_settings.value("Geometry/" + "frmGroundwaterEquationDeep_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmGroundwaterEquationDeep_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmGroundwaterEquationDeep_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        self.project = project
        gwf_section = self.project.gwf
        gwf_list = gwf_section.value[0:]
        for value in gwf_list:
            if (value.subcatchment_name == self.subcatchment_name and
                    value.groundwater_flow_type == GroundwaterFlowType.DEEP):
                self.txtControls.setPlainText(value.custom_equation)

    def cmdOK_Clicked(self):
        gwf_section = self._main_form.project.find_section("GWF")

        found = False
        for value in gwf_section.value:
            if (value.subcatchment_name == self.subcatchment_name and
                    value.groundwater_flow_type == GroundwaterFlowType.DEEP):
                found = True
                if value.custom_equation != self.txtControls.toPlainText():
                    self._main_form.mark_project_as_unsaved()
                value.custom_equation = self.txtControls.toPlainText()

                # no equation present, but previously had an equation,
                # so need to remove from gwf list
                if not self.txtControls.toPlainText():
                    gwf_section.value.remove(value)
                    self._main_form.mark_project_as_unsaved()

        if not found and self.txtControls.toPlainText():
            new_gwf = GWF()
            new_gwf.subcatchment_name = self.subcatchment_name
            new_gwf.groundwater_flow_type = GroundwaterFlowType.DEEP
            new_gwf.custom_equation = self.txtControls.toPlainText()
            self._main_form.project.gwf.value.append(new_gwf)
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmGroundwaterEquationDeep_geometry",
                                                  self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmGroundwaterEquationDeep_state",
                                                  self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
