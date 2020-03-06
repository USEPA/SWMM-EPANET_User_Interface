import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.SWMM.frmControlsDesigner import Ui_frmControls


class frmControls(QMainWindow, Ui_frmControls):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)

        self.set_from(main_form.project)
        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmControls_geometry") and
                main_form.program_settings.value("Geometry/" + "frmControls_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmControls_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmControls_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        # section = core.epanet.project.Control()

        self.txtControls.setPlainText(str(project.controls.value))

    def cmdOK_Clicked(self):
        if str(self.txtControls.toPlainText()) != self._main_form.project.controls.value:
            self._main_form.mark_project_as_unsaved()
        self._main_form.project.controls.value = str(self.txtControls.toPlainText())

        self._main_form.program_settings.setValue("Geometry/" + "frmControls_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmControls_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmControls_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmControls_state", self.saveState())
        self.close()
