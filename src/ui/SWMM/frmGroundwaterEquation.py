import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from ui.SWMM.frmGroundwaterEquationDesigner import Ui_frmGroundwaterEquation
from core.swmm.hydrology.subcatchment import GWF, GroundwaterFlowType


class frmGroundwaterEquation(QMainWindow, Ui_frmGroundwaterEquation):

    def __init__(self, main_form, subcatchment_name):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/groundwater_equation_editor.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.setupUi(self)
        self.subcatchment_name = subcatchment_name
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)

    def set_from(self, project):
        self.project = project
        gwf_section = self.project.gwf
        for value in gwf_section.value:
            if (value.subcatchment_name == self.subcatchment_name and
                    value.groundwater_flow_type == GroundwaterFlowType.LATERAL):
                self.txtControls.setPlainText(value.custom_equation)

    def cmdOK_Clicked(self):
        gwf_section = self._main_form.project.find_section("GWF")

        found = False
        for value in gwf_section.value:
            if (value.subcatchment_name == self.subcatchment_name and
                    value.groundwater_flow_type == GroundwaterFlowType.LATERAL):
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
            new_gwf.groundwater_flow_type = GroundwaterFlowType.LATERAL
            new_gwf.custom_equation = self.txtControls.toPlainText()
            self._main_form.project.gwf.value.append(new_gwf)
            self._main_form.mark_project_as_unsaved()

        self.close()

    def cmdCancel_Clicked(self):
        self.close()
