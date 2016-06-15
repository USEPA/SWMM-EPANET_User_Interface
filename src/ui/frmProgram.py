from PyQt4 import QtCore, QtGui
from frmProgramDesigner import Ui_program

class frmProgram(QtGui.QDialog):
    def __init__(self, main_form=None):
        QtGui.QDialog.__init__(self)
        self._main_form = main_form
        self.model = ''
        self.ui = Ui_program()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.btnEPANET, QtCore.SIGNAL('clicked()'), self.select_program_epanet)
        QtCore.QObject.connect(self.ui.btnSWMM, QtCore.SIGNAL('clicked()'), self.select_program_swmm)

    def select_program_epanet(self):
        self.model = 'EPANET'
        self.accept()

    def select_program_swmm(self):
        self.model = 'SWMM'
        self.accept()

    def getModel(self):
        return self.model


