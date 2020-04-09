import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.SWMM.frmAboutDesigner import Ui_frmAbout


class frmAbout(QMainWindow, Ui_frmAbout):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmAbout_geometry") and
                main_form.program_settings.value("Geometry/" + "frmAbout_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmAbout_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmAbout_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def cmdOK_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmAbout_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmAbout_state", self.saveState())
        self.close()
