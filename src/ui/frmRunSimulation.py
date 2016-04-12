import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.frmRunSimulationDesigner import Ui_frmRunSimulation


class frmRunSimulation(QtGui.QMainWindow, Ui_frmRunSimulation):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdStop, QtCore.SIGNAL("clicked()"), self.cmdStop_Clicked)
        QtCore.QObject.connect(self.cmdMinimize, QtCore.SIGNAL("clicked()"), self.cmdMinimize_Clicked)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        # self.set_from(parent.project)
        self._parent = parent

    # def set_from(self, project):

    def cmdOK_Clicked(self):
        self.close()

    def cmdMinimize_Clicked(self):
        self.close()

    def cmdStop_Clicked(self):
        self.close()
