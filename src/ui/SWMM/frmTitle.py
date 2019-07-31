import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.swmm.swmm_project
from ui.SWMM.frmTitleDesigner import Ui_frmTitle


class frmTitle(QMainWindow, Ui_frmTitle):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        self.txtTitle.setPlainText(project.title.title)

    def cmdOK_Clicked(self):
        section = self._main_form.project.title
        if section.title != self.txtTitle.toPlainText():
            self._main_form.mark_project_as_unsaved()
        section.title = self.txtTitle.toPlainText()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
