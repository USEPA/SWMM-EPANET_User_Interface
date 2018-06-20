import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.EPANET.frmControlsDesigner import Ui_frmControls


class frmControls(QMainWindow, Ui_frmControls):

    def __init__(self, main_form, title, control_type):
        QMainWindow.__init__(self, main_form)
        if title == "EPANET Simple Controls":
            self.help_topic = "epanet/src/src/Simple_C.htm"
        else:
            self.help_topic = "epanet/src/src/Rule-Bas.htm"
        self.setupUi(self)
        if title:
            self.setWindowTitle(title)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self._main_form = main_form
        self.control_type = control_type
        if main_form and main_form.project and control_type:
            self.set_from(main_form.project, control_type)

    def set_from(self, project, control_type):
        # section = core.epanet.project.Control()
        self.control_type = control_type
        section = project.find_section(control_type)
        self.txtControls.setPlainText(section.value)

    def cmdOK_Clicked(self):
        section = self._main_form.project.find_section(self.control_type)
        section.value = str(self.txtControls.toPlainText())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
