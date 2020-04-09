from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog
from frmProgramDesigner import Ui_program

class frmProgram(QDialog):
    def __init__(self, main_form=None):
        QDialog.__init__(self)
        self._main_form = main_form
        self.model = ''
        self.ui = Ui_program()
        self.ui.setupUi(self)
        self.ui.btnEPANET.clicked.connect(self.select_program_epanet)
        self.ui.btnSWMM.clicked.connect(self.select_program_swmm)

    def select_program_epanet(self):
        self.model = 'EPANET'
        self.accept()

    def select_program_swmm(self):
        self.model = 'SWMM'
        self.accept()

    def getModel(self):
        return self.model


