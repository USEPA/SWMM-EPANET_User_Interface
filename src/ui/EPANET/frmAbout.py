import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.EPANET.frmAboutDesigner import Ui_frmAbout


class frmAbout(QtGui.QMainWindow, Ui_frmAbout):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        self._main_form = main_form

    def cmdOK_Clicked(self):
        self.close()
