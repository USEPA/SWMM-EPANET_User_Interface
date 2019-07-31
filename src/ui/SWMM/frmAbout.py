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

    def cmdOK_Clicked(self):
        self.close()
