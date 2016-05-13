import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.EPANET.frmGraphDesigner import Ui_frmGraph


class frmGraph(QtGui.QMainWindow, Ui_frmGraph):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._parent = parent
        # self.set_from(parent.project)

    # def set_from(self, project):
        # section = core.epanet.project.Control()
        # section = project.find_section(control_type)
        # self.txtControls.setPlainText(str(section.get_text()))

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section(self.control_type)
        section.set_text(str(self.txtControls.toPlainText()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
