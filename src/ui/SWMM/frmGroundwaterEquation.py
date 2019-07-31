import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from ui.SWMM.frmGroundwaterEquationDesigner import Ui_frmGroundwaterEquation


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
        groundwater_section = self.project.groundwater
        for value in groundwater_section.value:
            if value.subcatchment == self.subcatchment_name:
                self.txtControls.setPlainText(value.custom_lateral_flow_equation)

    def cmdOK_Clicked(self):
        groundwater_section = self.project.groundwater
        for value in groundwater_section.value:
            if value.subcatchment == self.subcatchment_name:
                if value.custom_lateral_flow_equation != self.txtControls.toPlainText():
                    self._main_form.session.mark_project_as_unsaved()
                value.custom_lateral_flow_equation = self.txtControls.toPlainText()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
