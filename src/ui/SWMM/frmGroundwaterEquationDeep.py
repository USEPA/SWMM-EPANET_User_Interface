import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
from ui.SWMM.frmGroundwaterEquationDeepDesigner import Ui_frmGroundwaterEquationDeep


class frmGroundwaterEquationDeep(QtGui.QMainWindow, Ui_frmGroundwaterEquationDeep):

    def __init__(self, main_form, subcatchment_name):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/groundwater_equation_editor.htm"
        self.setupUi(self)
        self.subcatchment_name = subcatchment_name
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(main_form.project)

    def set_from(self, project):
        self.project = project
        groundwater_section = self.project.groundwater
        groundwater_list = groundwater_section.value[0:]
        for value in groundwater_list:
            if value.subcatchment == self.subcatchment_name:
                self.txtControls.setPlainText(value.custom_deep_flow_equation)

    def cmdOK_Clicked(self):
        groundwater_section = self.project.groundwater
        groundwater_list = groundwater_section.value[0:]
        for value in groundwater_list:
            if value.subcatchment == self.subcatchment_name:
                value.custom_deep_flow_equation = self.txtControls.toPlainText()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
